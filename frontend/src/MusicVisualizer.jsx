import React, { useState, useEffect, useCallback, useRef } from 'react';
// Rely on NPM installed packages for icons (Lucide)
import { Upload, Music, Loader, Wand, Info } from 'lucide-react';

// --- Loading Spinner Component: Stylized Sine Wave and Trivia ---
const LoadingSpinner = ({ loadingMessage }) => {
  const [trivia, setTrivia] = useState("Loading musicological facts...");
  const [loadingStep, setLoadingStep] = useState(0);

  // Fetch trivia loop
  useEffect(() => {
    let isMounted = true;
    const fetchTrivia = async () => {
      try {
        // Use exponential backoff for a more robust fetch
        const response = await fetch(`/api/trivia`);
        const data = await response.json();
        if (isMounted) {
          setTrivia(data.trivia);
          setLoadingStep(prev => (prev + 1) % 4);
        }
      } catch (e) {
        if (isMounted) setTrivia("The silence between the notes is music, too.");
      }
    };
    
    // Initial fetch and set interval for subsequent fetches
    fetchTrivia();
    const intervalId = setInterval(fetchTrivia, 15000);
    
    return () => { 
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);
  
  // Custom Sine Wave Loading Indicator
  const SineWave = () => (
    <div className="flex justify-center items-center h-16 w-full overflow-hidden">
      {[...Array(8)].map((_, i) => (
        <div
          key={i}
          className="w-2 h-2 mx-1 bg-indigo-500 rounded-full animate-bounce"
          style={{ 
            animationDelay: `${i * 0.1}s`,
            animationDuration: '1.2s',
            transform: `translateY(${Math.sin((i / 8) * Math.PI * 2) * 50}%)`,
          }}
        ></div>
      ))}
    </div>
  );

  return (
    <div className="flex flex-col items-center justify-center p-8 bg-white/90 backdrop-blur-sm rounded-xl shadow-2xl transition-all duration-500 w-full max-w-lg">
      <SineWave />
      <h2 className="text-xl font-bold text-gray-800 my-4 flex items-center">
        <Loader className="animate-spin mr-2 h-5 w-5 text-indigo-600" />
        {loadingMessage}
      </h2>
      <div className="w-full h-1 bg-indigo-100 rounded-full my-4">
        <div 
          className="h-full bg-indigo-500 rounded-full transition-all duration-500 ease-in-out" 
          style={{ width: `${(loadingStep / 4) * 100}%` }}
        ></div>
      </div>
      <div className="mt-4 p-4 bg-indigo-50 rounded-lg text-sm italic text-gray-600 border-l-4 border-indigo-400 min-h-[5rem] flex items-center">
        <p>"{trivia}"</p>
      </div>
    </div>
  );
};

// --- Main App Component ---
const App = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setResult(null);
      setError(null);
    } else {
      // Custom modal replacement for alert()
      setError("File must be a PDF. Please select your sheet music file again.");
      setFile(null);
    }
  };

  const processFile = useCallback(async (isRegenerate = false) => {
    if (!file && !isRegenerate) return; 
    setIsLoading(true);
    setError(null);

    try {
      let endpoint = isRegenerate ? 'regenerate' : 'process-music';
      let method = 'POST';
      let body;
      let headers = {};

      if (!isRegenerate) {
        const formData = new FormData();
        formData.append('file', file);
        body = formData;
      } else {
        // Regeneration only needs to signal the server
        body = JSON.stringify({}); 
        headers['Content-Type'] = 'application/json';
      }

      const response = await fetch(`/api/${endpoint}`, {
        method: method,
        headers: headers,
        body: body,
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(data.error || `Server error during ${isRegenerate ? 'regeneration' : 'processing'}.`);
      }
      
      setResult(data);

    } catch (e) {
      console.error(e);
      // Clean up file state if the initial upload failed
      if (!isRegenerate) setFile(null); 
      setError(`Processing failed: ${e.message}.`);
    } finally {
      setIsLoading(false);
    }
  }, [file]);

  // Automatically start processing when a valid file is selected
  useEffect(() => {
    if (file && !isLoading && !result) {
      processFile(false);
    }
  }, [file, isLoading, result, processFile]);


  // --- UI Components ---
  const IntroCard = (
    <div className="bg-white/95 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-indigo-100 transition-all duration-300">
      <h1 className="text-4xl font-extrabold text-indigo-700 mb-4 flex items-center">
        <Music className="w-8 h-8 mr-3 text-indigo-500" />
        ScoreSense
      </h1>
      <p className="text-gray-600 mb-6 leading-relaxed">
        **ScoreSense** translates complex sheet music into accessible visual art and simple narration. This service helps **novices, students, and those with hearing impairments** gain an intuitive understanding of a piece's core **structure, rhythm, and emotional dynamics**.
      </p>
      
      <button
        onClick={() => fileInputRef.current.click()}
        className="w-full flex items-center justify-center px-6 py-3 border border-transparent text-lg font-semibold rounded-xl text-white bg-indigo-600 hover:bg-indigo-700 transition duration-150 ease-in-out shadow-lg transform hover:scale-[1.02]"
      >
        <Upload className="w-5 h-5 mr-2" />
        Upload Sheet Music (PDF Only)
      </button>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept=".pdf"
        className="hidden"
      />
      {error && <p className="mt-4 text-red-500 text-sm font-medium p-3 bg-red-50 rounded-lg">{error}</p>}
    </div>
  );

  const ResultDisplay = (
    <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl transition-all duration-500 w-full overflow-hidden border border-indigo-200">
      <div className="p-6 bg-indigo-50 border-b border-indigo-100">
        <h2 className="text-2xl font-bold text-indigo-700">
          Visualizing: {result?.title || 'Score'}
        </h2>
        <p className="text-sm text-gray-500 mt-1 flex items-center">
          <Wand className="w-4 h-4 mr-1 text-indigo-400" />
          Visualization Style: **{result?.visualization_type || 'Abstract'}**
        </p>
      </div>

      <div className="flex flex-col lg:flex-row">
        {/* Left Side: Image Display */}
        <div className="w-full lg:w-1/2 p-6 flex justify-center items-center bg-gray-50">
          {result?.image_base64 ? (
            <div className="w-full h-auto max-w-md aspect-square rounded-xl shadow-xl overflow-hidden transform hover:scale-[1.02] transition-transform duration-300 ring-4 ring-indigo-300/50">
                {/* The image data is pre-pended with the mime-type */}
                <img 
                    src={`data:image/png;base64,${result.image_base64}`} 
                    alt={`Visualization of ${result.title} in ${result.visualization_type} style`}
                    className="w-full h-full object-cover"
                />
            </div>
          ) : (
            <div className="w-full h-64 flex items-center justify-center text-gray-400">Image not available</div>
          )}
        </div>

        {/* Right Side: Narration and Controls */}
        <div className="w-full lg:w-1/2 p-6 lg:p-8 flex flex-col justify-between">
          <div>
            <h3 className="text-xl font-bold text-gray-800 mb-3 border-b pb-2">Narrative for Non-Musicians:</h3>
            <p className="text-lg text-gray-700 italic leading-relaxed bg-indigo-50 p-4 rounded-lg border-l-4 border-indigo-500">
              {result?.narration || 'Narrative not available.'}
            </p>
          </div>
          
          <div className="mt-6 pt-4 border-t border-gray-200">
            <button
              onClick={() => processFile(true)}
              disabled={isLoading}
              className="w-full flex items-center justify-center px-6 py-3 text-lg font-semibold rounded-xl text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-400 transition duration-150 ease-in-out shadow-md"
            >
              <Wand className="w-5 h-5 mr-2" />
              Generate Another Visual Style
            </button>
            <button
              onClick={() => fileInputRef.current.click()}
              className="w-full flex items-center justify-center mt-3 px-6 py-2 text-md font-medium rounded-xl text-indigo-700 bg-indigo-100 hover:bg-indigo-200 transition duration-150 ease-in-out"
            >
              <Upload className="w-4 h-4 mr-2" />
              Upload New Sheet Music
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-8 flex flex-col items-center">
      <div className="w-full max-w-4xl py-12">
        {isLoading && <LoadingSpinner loadingMessage={result?.music_data ? "Generating New Visual..." : "Analyzing Sheet Music..."} />}
        
        {!isLoading && !result && IntroCard}

        {!isLoading && result && ResultDisplay}

        {/* Disclaimer Section */}
        {result?.disclaimer && (
            <div className="w-full max-w-4xl mt-10 p-4 bg-yellow-50 rounded-xl border border-yellow-200 flex items-start text-sm text-yellow-800 shadow-inner">
              <Info className="w-5 h-5 mr-3 mt-1 flex-shrink-0" />
              <p>
                **Visualization Consistency Disclaimer:** {result.disclaimer}
              </p>
            </div>
        )}
      </div>
    </div>
  );
};

export default App;