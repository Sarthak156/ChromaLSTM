import { useState, useRef } from 'react';
import { Zap, Scan, Cpu, MoveHorizontal, RotateCcw, Download } from 'lucide-react';

function App() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [isDone, setIsDone] = useState(false);
  const [sliderVal, setSliderVal] = useState(50);
  const [error, setError] = useState(null);

  // State for holding image data
  const [originalImage, setOriginalImage] = useState(null); // The user's uploaded image (for B&W preview)
  const [colorizedImage, setColorizedImage] = useState(null); // The result from the API

  // Ref for the hidden file input
  const fileInputRef = useRef(null);

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Reset previous state
    reset();
    setError(null);

    // Create a URL for the original image to show a preview
    setOriginalImage(URL.createObjectURL(file));
    setIsProcessing(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to colorize image.');
      }

      const imageBlob = await response.blob();
      setColorizedImage(URL.createObjectURL(imageBlob));
      setIsDone(true);

    } catch (err) {
      console.error("API Error:", err);
      setError(err.message);
      reset(); // Clear out partial state on error
    } finally {
      setIsProcessing(false);
    }
  };

  const reset = () => {
    setIsProcessing(false);
    setIsDone(false);
    setOriginalImage(null);
    setColorizedImage(null);
    setSliderVal(50);
  };

  return (
    <div className="min-h-screen flex flex-col items-center pb-12">
      <nav className="w-full border-b-[3px] border-black px-6 py-3 flex justify-between items-center bg-brutalBg z-50 sticky top-0">
        <div className="flex items-center gap-2">
          <Zap className="w-6 h-6" />
          <span className="font-bold text-xl uppercase tracking-wider font-['Space_Grotesk']">xLSTM_COLOR.SYS</span>
        </div>
        <div className="border-[3px] border-black bg-brutalYellow px-3 py-1 font-mono text-sm uppercase shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] font-bold flex gap-2 items-center">
          <span className="w-2 h-2 rounded-full bg-black block animate-pulse"></span>
          [ STATUS: ONLINE ]
        </div>
      </nav>

      <main className="w-full max-w-[1300px] mt-12 px-6 grid grid-cols-1 gap-12 flex-grow">
        <header className="text-center flex flex-col items-center gap-6 mt-8">
          <h1 className="text-7xl lg:text-[96px] font-black uppercase leading-[0.9] tracking-tight font-['Space_Grotesk']">
            Intelligent<br />Image<br />Colorization.
          </h1>
          <p className="text-brutalSecondary text-xl max-w-2xl font-mono uppercase">
            Proprietary pure-pytorch matrix-LSTM analysis protocol for restoring chromatic data to monochrome optical captures.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-12 w-full">
          {/* Left Column */}
          <div className="col-span-1 flex flex-col gap-8">
            <div className="border-[3px] border-black bg-white p-6 shadow-brutal flex flex-col gap-4">
              <span className="text-brutalBlue font-mono text-sm uppercase font-bold">// ARCHITECTURE</span>
              <h2 className="text-3xl font-bold uppercase font-['Space_Grotesk']">System Specs</h2>
              <ul className="font-mono text-sm space-y-3 mt-4 border-t-[3px] border-black pt-4">
                <li className="flex justify-between items-center border-b border-black pb-2">
                  <span>ENGINE</span><span className="bg-black text-white px-2 py-0.5">xLSTM_v1</span>
                </li>
                <li className="flex justify-between items-center border-b border-black pb-2">
                  <span>DIMENSIONS</span><span className="bg-black text-white px-2 py-0.5">256px</span>
                </li>
              </ul>
            </div>
            
            <div className="border-[3px] border-black bg-white p-6 shadow-brutal flex flex-col gap-4">
              <span className="text-brutalBlue font-mono text-sm uppercase font-bold">// INPUT SECTOR</span>
              <h2 className="text-3xl font-bold uppercase font-['Space_Grotesk']">Load Data</h2>
              <div 
                className="border-[3px] border-black border-dashed mt-2 p-12 flex flex-col items-center justify-center gap-4 bg-brutalBg hover:bg-black hover:text-white transition-colors duration-200 cursor-pointer group disabled:cursor-not-allowed disabled:opacity-50"
                onClick={() => !isProcessing && fileInputRef.current.click()}
                disabled={isProcessing}
              >
                <Scan className="w-12 h-12" />
                <h3 className="text-2xl font-bold uppercase font-['Space_Grotesk']">{isProcessing ? 'Processing...' : 'Insert File'}</h3>
                <p className="font-mono text-sm text-center opacity-80 group-hover:opacity-100">Click to upload a .PNG or .JPG</p>
              </div>
              <input 
                type="file" 
                ref={fileInputRef} 
                className="hidden" 
                onChange={handleFileSelect} accept="image/png, image/jpeg" />
              {error && (
                <div className="border-[3px] border-brutalRed bg-brutalRed/10 text-brutalRed p-3 font-mono text-sm uppercase font-bold">{error}</div>
              )}
            </div>
          </div>

          {/* Right Column */}
          <div className="col-span-1 lg:col-span-2 flex flex-col gap-8">
            <div className="border-[3px] border-black bg-white p-6 shadow-brutal flex flex-col h-full gap-4">
              <div className="flex justify-between items-end">
                <div>
                  <span className="text-brutalBlue font-mono text-sm uppercase font-bold">// OUTPUT TERMINAL</span>
                  <h2 className="text-3xl font-bold uppercase font-['Space_Grotesk']">Analysis Result</h2>
                </div>
                {isDone && (
                  <div><span className="border-[3px] border-black bg-brutalGreen px-3 py-1 font-mono text-sm uppercase font-bold">OPERATION COMPLETE</span></div>
                )}
              </div>

              {!originalImage && !isProcessing && (
                <div className="border-[3px] border-black bg-[#eee] h-[500px] flex items-center justify-center flex-col gap-4">
                  <Cpu className="w-16 h-16 opacity-30" />
                  <p className="font-mono uppercase opacity-50 font-bold">Awaiting target parameters...</p>
                </div>
              )}

              {isProcessing && (
                <div className="border-[3px] border-black bg-[#eee] h-[500px] flex items-center justify-center flex-col gap-4">
                  <div className="w-16 h-16 border-[4px] border-black border-t-brutalBlue rounded-full animate-spin"></div>
                  <p className="font-mono uppercase font-bold">Initializing Analysis Protocol...</p>
                </div>
              )}

              {isDone && originalImage && colorizedImage && (
                <>
                  <div className="relative border-[3px] border-black h-[500px] overflow-hidden bg-[#eee]">
                    {/* B&W Image (Original Upload) */}
                    <img src={originalImage} style={{filter: 'grayscale(100%)'}} className="absolute inset-0 w-full h-full object-cover" alt="Original Grayscale" />
                    {/* Color Image (From API) */}
                    <img src={colorizedImage} style={{clipPath: `polygon(0 0, ${sliderVal}% 0, ${sliderVal}% 100%, 0 100%)`}} className="absolute inset-0 w-full h-full object-cover" alt="Colorized Result" />
                    <input type="range" min="0" max="100" value={sliderVal} onChange={(e) => setSliderVal(e.target.value)} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
                    <div className="absolute top-0 w-[3px] h-full bg-black z-0 flex items-center justify-center" style={{left: `${sliderVal}%`}}>
                      <div className="w-8 h-8 bg-white border-[3px] border-black flex items-center justify-center">
                        <MoveHorizontal className="w-5 h-5" />
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-end gap-4 mt-4">
                    <button onClick={reset} className="border-[3px] border-black px-6 py-3 font-bold uppercase flex gap-2 items-center hover:bg-black hover:text-white transition-all bg-brutalBg shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:translate-y-1 active:translate-x-1 active:shadow-none">
                      <RotateCcw className="w-5 h-5" /> Reset
                    </button>
                    <a href={colorizedImage} download="colorized_image.png" className="border-[3px] border-black px-8 py-3 font-bold uppercase flex gap-2 items-center bg-black text-white hover:bg-white hover:text-black transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:translate-y-1 active:translate-x-1 active:shadow-none">
                      <Download className="w-5 h-5" /> Export PNG
                    </a>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;