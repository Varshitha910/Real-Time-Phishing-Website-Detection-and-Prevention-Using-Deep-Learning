// // Dashboard overview page with key system metrics.
// import MetricCard from "../components/MetricCard.jsx";
// import PageHeader from "../components/PageHeader.jsx";
// import RiskBadge from "../components/RiskBadge.jsx";

// const recentScans = [
//   { url: "https://example.com", prediction: "Legitimate", risk: "Low" },
//   { url: "http://secure-login.example-alert.com", prediction: "Phishing", risk: "High" },
//   { url: "https://accounts.example.net", prediction: "Suspicious", risk: "Medium" },
// ];

// function Dashboard() {
//   return (
//     <>
//       <PageHeader title="Dashboard" description="Monitor phishing detection activity and model risk signals." />
//       <div className="stats-grid">
//         <MetricCard label="Total Scans" value="0" />
//         <MetricCard label="Phishing Detected" value="0" />
//         <MetricCard label="Average Confidence" value="0%" />
//         <MetricCard label="High Risk URLs" value="0" />
//       </div>

//       <section className="card" style={{ marginTop: 18 }}>
//         <h2>Recent Activity</h2>
//         <table className="table">
//           <thead>
//             <tr>
//               <th>URL</th>
//               <th>Prediction</th>
//               <th>Risk</th>
//             </tr>
//           </thead>
//           <tbody>
//             {recentScans.map((scan) => (
//               <tr key={scan.url}>
//                 <td>{scan.url}</td>
//                 <td>{scan.prediction}</td>
//                 <td>
//                   <RiskBadge riskLevel={scan.risk} />
//                 </td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </section>
//     </>
//   );
// }

// export default Dashboard;


// import {useEffect,useState} from "react";
// import MetricCard from "../components/MetricCard.jsx";
// import PageHeader from "../components/PageHeader.jsx";
// import RiskBadge from "../components/RiskBadge.jsx";


// function Dashboard(){

// const [stats,setStats]=useState({
// total_scans:0,
// phishing_count:0,
// safe_count:0,
// critical_count:0
// });


// useEffect(()=>{

// fetch("http://127.0.0.1:8000/api/analytics/summary")
// .then(res=>res.json())
// .then(data=>{
// setStats(data)
// })

// },[]);



// return(
// <>

// <PageHeader 
// title="Dashboard"
// description="Monitor phishing detection activity and model risk signals."
// />


// <div className="stats-grid">


// <MetricCard 
// label="Total Scans"
// value={stats.total_scans}
// />


// <MetricCard 
// label="Phishing Detected"
// value={stats.phishing_count}
// />


// <MetricCard 
// label="Average Confidence"
// value="Live"
// />


// <MetricCard 
// label="High Risk URLs"
// value={stats.critical_count}
// />


// </div>



// <section className="card">

// <h2>Recent Activity</h2>


// <p>
// Dashboard is connected with MongoDB scan history.
// </p>


// </section>


// </>

// )

// }

// export default Dashboard;

// import MetricCard from "../components/MetricCard.jsx";
// import PageHeader from "../components/PageHeader.jsx";
// import RiskBadge from "../components/RiskBadge.jsx";


// const recentScans=[

// {
// url:"https://www.google.com",
// prediction:"Legitimate",
// risk:"No Risk"
// },

// {
// url:"http://paypal-login-security-update.com",
// prediction:"Phishing",
// risk:"High Risk"
// },

// {
// url:"http://account-verification-required.com",
// prediction:"Phishing",
// risk:"High Risk"
// }

// ];


// function Dashboard(){


// return (

// <>


// <PageHeader
// title="Dashboard"
// description="Monitor phishing detection activity and model risk signals."
// />



// <div className="stats-grid">


// <MetricCard
// label="Total Scans"
// value="44"
// />


// <MetricCard
// label="Phishing Detected"
// value="9"
// />


// <MetricCard
// label="Average Confidence"
// value="95%"
// />


// <MetricCard
// label="High Risk URLs"
// value="7"
// />


// </div>




// <section className="card"
// style={{marginTop:18}}>


// <h2>
// Recent Activity
// </h2>



// <table className="table">

// <thead>

// <tr>

// <th>URL</th>
// <th>Prediction</th>
// <th>Risk</th>

// </tr>

// </thead>


// <tbody>


// {
// recentScans.map((scan)=>(


// <tr key={scan.url}>


// <td>
// {scan.url}
// </td>


// <td>
// {scan.prediction}
// </td>


// <td>

// <RiskBadge
// riskLevel={scan.risk}
// />

// </td>


// </tr>


// ))
// }


// </tbody>

// </table>



// </section>



// </>

// )

// }


// export default Dashboard;

import { useEffect, useState } from "react";
import MetricCard from "../components/MetricCard.jsx";
import PageHeader from "../components/PageHeader.jsx";

function Dashboard() {
  const [stats, setStats] = useState({
    total_scans: 0,
    phishing_count: 0,
    critical_count: 0,
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/analytics/summary")
      .then((res) => res.json())
      .then((data) => setStats(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <>
      <PageHeader
        title="Dashboard"
        description="Monitor phishing detection activity and model risk signals."
      />

      <div className="stats-grid">
        <MetricCard
          label="Total Scans"
          value={stats.total_scans}
        />

        <MetricCard
          label="Phishing Detected"
          value={stats.phishing_count}
        />

        <MetricCard
          label="Average Confidence"
          value="95%"
        />

        <MetricCard
          label="High Risk URLs"
          value={stats.critical_count}
        />
      </div>
    </>
  );
}

export default Dashboard;