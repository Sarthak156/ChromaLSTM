import torch
import torch.nn as nn

# This is a new block implementation that matches the keys found in your checkpoint file.
# It replaces the old `PurePyTorch_mLSTM_Block`.
class mLSTMBlock(nn.Module):
    def __init__(self, embed_dim):
        super().__init__()
        # LayerNorm expects bias=False
        self.xlstm_norm = nn.LayerNorm(embed_dim, bias=False)
        # This nested structure is required to match the keys like "xlstm.proj_up.weight"
        self.xlstm = nn.Module()
        # learnable_skip should have size of embed_dim
        self.xlstm.learnable_skip = nn.Parameter(torch.randn(embed_dim))
        # proj_up should be embed_dim -> embed_dim * 2, with bias=False
        self.xlstm.proj_up = nn.Linear(embed_dim, embed_dim * 2, bias=False)
        # All these projections should have bias=False
        self.xlstm.q_proj = nn.Linear(embed_dim * 2, embed_dim * 2, bias=False)
        self.xlstm.k_proj = nn.Linear(embed_dim * 2, embed_dim * 2, bias=False)
        self.xlstm.v_proj = nn.Linear(embed_dim * 2, embed_dim * 2, bias=False)
        # Matching the Conv1D block from the checkpoint keys
        self.xlstm.conv1d = nn.Module()
        self.xlstm.conv1d.conv = nn.Conv1d(embed_dim * 2, embed_dim * 2, kernel_size=3, padding=1, groups=embed_dim*2)
        # Matching the mLSTM cell keys
        self.xlstm.mlstm_cell = nn.Module()
        self.xlstm.mlstm_cell.igate = nn.Linear(embed_dim * 2, embed_dim * 2)
        self.xlstm.mlstm_cell.fgate = nn.Linear(embed_dim * 2, embed_dim * 2)
        self.xlstm.mlstm_cell.outnorm = nn.LayerNorm(embed_dim * 2, bias=False)
        self.xlstm.proj_down = nn.Linear(embed_dim * 2, embed_dim, bias=False)

    def forward(self, x):
        # This forward pass is a placeholder. The main goal is to create a class
        # with the correct layer names so that `load_state_dict` can find them.
        raise NotImplementedError("This block is for architecture matching only.")

class xLSTMColorizer(nn.Module):
    def __init__(self, embed_dim=256, num_blocks=4):
        super().__init__()
        # The encoder and decoder are likely correct.
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(64), nn.ReLU(True),
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128), nn.ReLU(True),
            nn.Conv2d(128, embed_dim, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(embed_dim), nn.ReLU(True),
            nn.Conv2d(embed_dim, embed_dim, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(embed_dim), nn.ReLU(True),
        )
        self.embed_dim = embed_dim
        # This structure matches the "xlstm.blocks.0..." key format
        self.xlstm = nn.Module()
        self.xlstm.blocks = nn.ModuleList([mLSTMBlock(embed_dim) for _ in range(num_blocks)])
        self.xlstm.post_blocks_norm = nn.LayerNorm(embed_dim, bias=False)

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(embed_dim, embed_dim, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(embed_dim), nn.ReLU(True),
            nn.ConvTranspose2d(embed_dim, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128), nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(64), nn.ReLU(True),
            nn.ConvTranspose2d(64, 2, kernel_size=4, stride=2, padding=1),
            nn.Tanh()
        )
        
    def forward(self, x):
        B = x.shape[0]
        encoded = self.encoder(x)
        _, _, H, W = encoded.shape
        x = encoded.view(B, self.embed_dim, -1).permute(0, 2, 1)
        # A placeholder forward pass for the new structure
        for block in self.xlstm.blocks:
            x = x + 0 # Pass through a dummy block
        x = self.xlstm.post_blocks_norm(x)
        x = x.permute(0, 2, 1).contiguous().view(B, self.embed_dim, H, W)
        out = self.decoder(x)
        return out
