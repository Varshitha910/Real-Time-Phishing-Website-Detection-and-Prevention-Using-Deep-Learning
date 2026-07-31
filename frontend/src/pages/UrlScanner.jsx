// // URL Scanner page. It submits URLs to the FastAPI /predict endpoint and
// // presents the model prediction, confidence, and risk level with loading and
// // error states.
// import { AlertTriangle, CheckCircle2, Loader2, ScanSearch, ShieldAlert } from "lucide-react";
// import { useState } from "react";
// import { predictUrl } from "../services/detectionService.js";

// function URLScanner() {
//   const [url, setUrl] = useState("");
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState("");
//   const [loading, setLoading] = useState(false);

//   async function handleSubmit(event) {
//     event.preventDefault();

//     const trimmedUrl = url.trim();
//     if (!trimmedUrl) {
//       setError("Enter a URL before scanning.");
//       setResult(null);
//       return;
//     }

//     setLoading(true);
//     setError("");
//     setResult(null);

//     try {
//       const prediction = await predictUrl(trimmedUrl);
//       setResult(prediction);
//     } catch (requestError) {
//       setError(requestError.response?.data?.detail || "Unable to scan this URL. Check the backend and try again.");
//     } finally {
//       setLoading(false);
//     }
//   }

//   const riskClass = getRiskClass(result?.risk_level);
//   const ResultIcon = result?.prediction === "Phishing" ? ShieldAlert : CheckCircle2;

//   return (
//     <div className="scanner-page">
//       <header className="scanner-header">
//         <div>
//           <p className="eyebrow">Real-time detection</p>
//           <h1>URL Scanner</h1>
//           <p className="scanner-copy">Analyze a website URL using the trained phishing detection model.</p>
//         </div>
//       </header>

//       <section className="scanner-panel">
//         <form onSubmit={handleSubmit} className="scanner-form">
//           <label htmlFor="scanner-url">Website URL</label>
//           <div className="scanner-input-row">
//             <input
//               id="scanner-url"
//               className="scanner-input"
//               type="url"
//               value={url}
//               onChange={(event) => setUrl(event.target.value)}
//               placeholder="https://example.com"
//               disabled={loading}
//             />
//             <button className="scanner-button" type="submit" disabled={loading || !url.trim()}>
//               {loading ? <Loader2 className="spin" size={18} aria-hidden="true" /> : <ScanSearch size={18} aria-hidden="true" />}
//               <span>{loading ? "Scanning" : "Scan"}</span>
//             </button>
//           </div>
//         </form>

//         {error ? (
//           <div className="scanner-alert" role="alert">
//             <AlertTriangle size={18} aria-hidden="true" />
//             <span>{error}</span>
//           </div>
//         ) : null}
//       </section>

//       {result ? (
//         <section className={`scanner-result ${riskClass}`} aria-live="polite">
//           <div className="result-icon">
//             <ResultIcon size={26} aria-hidden="true" />
//           </div>
//           <div>
//             <p className="result-label">Prediction</p>
//             <h2>{result.prediction}</h2>
//           </div>
//           <div>
//             <p className="result-label">Confidence</p>
//             <h2>{Number(result.confidence).toFixed(2)}%</h2>
//           </div>
//           <div>
//             <p className="result-label">Risk Level</p>
//             <h2>{result.risk_level}</h2>
//           </div>
//         </section>
//       ) : (
//         <section className="scanner-empty">
//           <ScanSearch size={34} aria-hidden="true" />
//           <p>Scan results will appear here.</p>
//         </section>
//       )}
//     </div>
//   );
// }

// function getRiskClass(riskLevel) {
//   const normalized = String(riskLevel || "").toLowerCase();
//   if (normalized === "high") {
//     return "result-high";
//   }
//   if (normalized === "medium") {
//     return "result-medium";
//   }
//   return "result-low";
// }

// export default URLScanner;


// import { AlertTriangle, CheckCircle2, Loader2, ScanSearch, ShieldAlert } from "lucide-react";
// import { useState } from "react";
// import { predictUrl } from "../services/detectionService.js";

// function URLScanner() {
//   const [url, setUrl] = useState("");
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState("");
//   const [loading, setLoading] = useState(false);

//   async function handleSubmit(event) {
//     event.preventDefault();

//     const trimmedUrl = url.trim();

//     if (!trimmedUrl) {
//       setError("Enter a URL before scanning.");
//       return;
//     }

//     setLoading(true);
//     setError("");
//     setResult(null);

//     try {
//       const prediction = await predictUrl(trimmedUrl);
//       setResult(prediction);
//     } catch (requestError) {
//       setError(
//         requestError.response?.data?.detail ||
//         "Unable to scan this URL. Check backend."
//       );
//     } finally {
//       setLoading(false);
//     }
//   }


//   function displayRisk(risk){
//     const value = String(risk).toLowerCase();

//     if(value==="safe"){
//       return "No Risk";
//     }

//     if(value==="suspicious"){
//       return "Medium Risk";
//     }

//     if(value==="phishing"){
//       return "High Risk";
//     }

//     return "Critical Risk";
//   }


//   const riskClass =
//     String(result?.risk_level).toLowerCase()==="phishing"
//       ? "result-high"
//       : String(result?.risk_level).toLowerCase()==="suspicious"
//       ? "result-medium"
//       : "result-low";


//   const ResultIcon =
//     result?.prediction==="Phishing"
//       ? ShieldAlert
//       : CheckCircle2;


// return (
// <div className="scanner-page">


// <header className="scanner-header">

// <div>

// <p className="eyebrow">
// Real-time detection
// </p>

// <h1>URL Scanner</h1>

// <p className="scanner-copy">
// Analyze a website URL using the trained phishing detection model.
// </p>

// </div>

// </header>



// <section className="scanner-panel">


// <form onSubmit={handleSubmit}
// className="scanner-form">


// <label>
// Website URL
// </label>


// <div className="scanner-input-row">


// <input
// className="scanner-input"
// type="text"
// placeholder="https://example.com"
// value={url}
// disabled={loading}
// onChange={(e)=>setUrl(e.target.value)}
// />



// <button
// className="scanner-button"
// disabled={loading}
// >

// {
// loading
// ?
// <Loader2 className="spin" size={18}/>
// :
// <ScanSearch size={18}/>
// }


// <span>
// {
// loading ? "Scanning":"Scan"
// }
// </span>


// </button>


// </div>


// </form>



// {
// error &&
// <div className="scanner-alert">

// <AlertTriangle size={18}/>

// <span>{error}</span>

// </div>
// }


// </section>



// {
// result ?

// <section className={`scanner-result ${riskClass}`}>



// <div className="result-icon">

// <ResultIcon size={26}/>

// </div>



// <div>

// <p className="result-label">
// Prediction
// </p>

// <h2>
// {result.prediction}
// </h2>

// </div>




// <div>

// <p className="result-label">
// Confidence
// </p>

// <h2>
// {Number(result.confidence).toFixed(2)}%
// </h2>

// </div>




// <div>

// <p className="result-label">
// Risk Level
// </p>

// {<h2>
// {displayRisk(result.risk_level, result.prediction)}
// </h2> }

// </div>


// </section>


// :

// <section className="scanner-empty">

// <ScanSearch size={34}/>

// <p>
// Scan results will appear here.
// </p>


// </section>

// }



// </div>

// );

// }


// export default URLScanner;
// import {
//   AlertTriangle,
//   CheckCircle2,
//   Loader2,
//   ScanSearch,
//   ShieldAlert,
// } from "lucide-react";
// import { useState } from "react";
// import { predictUrl } from "../services/detectionService.js";

// function URLScanner() {
//   const [url, setUrl] = useState("");
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState("");
//   const [loading, setLoading] = useState(false);

//   async function handleSubmit(event) {
//     event.preventDefault();

//     const trimmedUrl = url.trim();

//     if (!trimmedUrl) {
//       setError("Enter a URL before scanning.");
//       setResult(null);
//       return;
//     }

//     setLoading(true);
//     setError("");
//     setResult(null);

//     try {
//       const prediction = await predictUrl(trimmedUrl);
//       setResult(prediction);
//     } catch (requestError) {
//       setError(
//         requestError.response?.data?.detail ||
//           "Unable to scan this URL. Check the backend and try again."
//       );
//     } finally {
//       setLoading(false);
//     }
//   }

//   function displayRisk(risk, prediction) {
//     if (String(prediction).toLowerCase() === "legitimate") {
//       return "No Risk";
//     }

//     const value = String(risk).toLowerCase();

//     if (value === "safe") {
//       return "No Risk";
//     }

//     if (value === "suspicious") {
//       return "Medium Risk";
//     }

//     if (value === "phishing") {
//       return "High Risk";
//     }

//     if (value === "critical") {
//       return "Critical Risk";
//     }

//     return "No Risk";
//   }

//   function getRiskClass(riskLevel, prediction) {
//     if (String(prediction).toLowerCase() === "legitimate") {
//       return "result-low";
//     }

//     const normalized = String(riskLevel || "").toLowerCase();

//     if (normalized === "critical" || normalized === "phishing") {
//       return "result-high";
//     }

//     if (normalized === "suspicious") {
//       return "result-medium";
//     }

//     return "result-low";
//   }

//   const riskClass = getRiskClass(
//     result?.risk_level,
//     result?.prediction
//   );

//   const ResultIcon =
//     String(result?.prediction).toLowerCase() === "phishing"
//       ? ShieldAlert
//       : CheckCircle2;

//   return (
//     <div className="scanner-page">
//       <header className="scanner-header">
//         <div>
//           <p className="eyebrow">Real-time detection</p>
//           <h1>URL Scanner</h1>
//           <p className="scanner-copy">
//             Analyze a website URL using the trained phishing detection model.
//           </p>
//         </div>
//       </header>

//       <section className="scanner-panel">
//         <form onSubmit={handleSubmit} className="scanner-form">
//           <label htmlFor="scanner-url">Website URL</label>

//           <div className="scanner-input-row">
//             <input
//               id="scanner-url"
//               className="scanner-input"
//               type="url"
//               value={url}
//               onChange={(event) => setUrl(event.target.value)}
//               placeholder="https://example.com"
//               disabled={loading}
//             />

//             <button
//               className="scanner-button"
//               type="submit"
//               disabled={loading || !url.trim()}
//             >
//               {loading ? (
//                 <Loader2
//                   className="spin"
//                   size={18}
//                   aria-hidden="true"
//                 />
//               ) : (
//                 <ScanSearch
//                   size={18}
//                   aria-hidden="true"
//                 />
//               )}

//               <span>{loading ? "Scanning" : "Scan"}</span>
//             </button>
//           </div>
//         </form>

//         {error ? (
//           <div className="scanner-alert" role="alert">
//             <AlertTriangle size={18} aria-hidden="true" />
//             <span>{error}</span>
//           </div>
//         ) : null}
//       </section>

//       {result ? (
//         <section
//           className={`scanner-result ${riskClass}`}
//           aria-live="polite"
//         >
//           <div className="result-icon">
//             <ResultIcon size={26} aria-hidden="true" />
//           </div>

//           <div>
//             <p className="result-label">Prediction</p>
//             <h2>{result.prediction}</h2>
//           </div>

//           <div>
//             <p className="result-label">Confidence</p>
//             <h2>
//               {Number(
//                 result.confidence ||
//                   result.confidence_score ||
//                   0
//               ).toFixed(2)}
//               %
//             </h2>
//           </div>

//           <div>
//             <p className="result-label">Risk Level</p>
//             <h2>
//               {displayRisk(
//                 result.risk_level,
//                 result.prediction
//               )}
//             </h2>
//           </div>
//         </section>
//       ) : (
//         <section className="scanner-empty">
//           <ScanSearch size={34} aria-hidden="true" />
//           <p>Scan results will appear here.</p>
//         </section>
//       )}
//     </div>
//   );
// }

// export default URLScanner;

import {
  AlertTriangle,
  CheckCircle2,
  Loader2,
  ScanSearch,
  ShieldAlert,
} from "lucide-react";
import { useState } from "react";
import { predictUrl } from "../services/detectionService.js";

function URLScanner() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedUrl = url.trim();

    if (!trimmedUrl) {
      setError("Enter a URL before scanning.");
      setResult(null);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const prediction = await predictUrl(trimmedUrl);
      setResult(prediction);
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "Unable to scan this URL. Check the backend and try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function displayRisk(riskLevel) {
    const value = String(riskLevel || "").toLowerCase();

    if (value === "high") {
      return "High Risk";
    }

    if (value === "medium") {
      return "Medium Risk";
    }

    if (value === "low" || value === "safe") {
      return "No Risk";
    }

    if (value === "critical") {
      return "Critical Risk";
    }

    return riskLevel;
  }

  function getRiskClass(riskLevel) {
    const value = String(riskLevel || "").toLowerCase();

    if (value === "critical" || value === "high") {
      return "result-high";
    }

    if (value === "medium" || value === "suspicious") {
      return "result-medium";
    }

    return "result-low";
  }

  const riskClass = getRiskClass(result?.risk_level);

  const ResultIcon =
    String(result?.prediction || "").toLowerCase() === "phishing"
      ? ShieldAlert
      : CheckCircle2;

  return (
    <div className="scanner-page">
      <header className="scanner-header">
        <div>
          <p className="eyebrow">Real-time detection</p>
          <h1>URL Scanner</h1>
          <p className="scanner-copy">
            Analyze a website URL using the trained phishing detection model.
          </p>
        </div>
      </header>

      <section className="scanner-panel">
        <form onSubmit={handleSubmit} className="scanner-form">
          <label htmlFor="scanner-url">Website URL</label>

          <div className="scanner-input-row">
            <input
              id="scanner-url"
              className="scanner-input"
              type="url"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://example.com"
              disabled={loading}
            />

            <button
              className="scanner-button"
              type="submit"
              disabled={loading || !url.trim()}
            >
              {loading ? (
                <Loader2
                  className="spin"
                  size={18}
                  aria-hidden="true"
                />
              ) : (
                <ScanSearch
                  size={18}
                  aria-hidden="true"
                />
              )}

              <span>{loading ? "Scanning..." : "Scan"}</span>
            </button>
          </div>
        </form>

        {error && (
          <div className="scanner-alert" role="alert">
            <AlertTriangle size={18} />
            <span>{error}</span>
          </div>
        )}
      </section>

      {result ? (
        <section
          className={`scanner-result ${riskClass}`}
          aria-live="polite"
        >
          <div className="result-icon">
            <ResultIcon size={26} />
          </div>

          <div>
            <p className="result-label">Prediction</p>
            <h2>{result.prediction}</h2>
          </div>

          <div>
            <p className="result-label">Confidence</p>
            <h2>
              {Number(
                result.confidence ??
                  result.confidence_score ??
                  0
              ).toFixed(2)}
              %
            </h2>
          </div>

          <div>
            <p className="result-label">Risk Level</p>
            <h2>{displayRisk(result.risk_level)}</h2>
          </div>
        </section>
      ) : (
        <section className="scanner-empty">
          <ScanSearch size={34} />
          <p>Scan results will appear here.</p>
        </section>
      )}
    </div>
  );
}

export default URLScanner;