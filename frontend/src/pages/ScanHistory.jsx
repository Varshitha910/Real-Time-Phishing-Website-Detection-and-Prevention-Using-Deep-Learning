// // Scan history page for reviewing stored MongoDB prediction records.
// import PageHeader from "../components/PageHeader.jsx";
// import RiskBadge from "../components/RiskBadge.jsx";

// const placeholderHistory = [
//   {
//     id: "demo-1",
//     url: "https://example.com",
//     prediction: "Legitimate",
//     confidence: 98.4,
//     risk_level: "Low",
//     timestamp: "Pending MongoDB connection",
//   },
// ];

// function ScanHistory() {
//   return (
//     <>
//       <PageHeader title="Scan History" description="Review URLs analyzed by the phishing detection service." />
//       <section className="card">
//         <table className="table">
//           <thead>
//             <tr>
//               <th>URL</th>
//               <th>Prediction</th>
//               <th>Confidence</th>
//               <th>Risk</th>
//               <th>Timestamp</th>
//             </tr>
//           </thead>
//           <tbody>
//             {placeholderHistory.map((scan) => (
//               <tr key={scan.id}>
//                 <td>{scan.url}</td>
//                 <td>{scan.prediction}</td>
//                 <td>{scan.confidence}%</td>
//                 <td>
//                   <RiskBadge riskLevel={scan.risk_level} />
//                 </td>
//                 <td>{scan.timestamp}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </section>
//     </>
//   );
// }

// export default ScanHistory;


import {useEffect,useState} from "react";
import PageHeader from "../components/PageHeader.jsx";
import RiskBadge from "../components/RiskBadge.jsx";


function ScanHistory(){

const [history,setHistory]=useState([]);


useEffect(()=>{

fetch("http://127.0.0.1:8000/api/analytics/summary")
.then(res=>res.json())
.then(data=>{

console.log(data);

setHistory(data.daily_scans || []);

})
.catch(err=>console.log(err));

},[]);



return(
<>

<PageHeader
title="Scan History"
description="Review URLs analyzed by the phishing detection service."
/>


<section className="card">

<table className="table">

<thead>

<tr>
<th>Date</th>
<th>Total Scans</th>
<th>Status</th>
</tr>

</thead>


<tbody>

{
history.map((item,index)=>(

<tr key={index}>

<td>{item.date}</td>

<td>{item.count}</td>

<td>
<RiskBadge riskLevel="Low"/>
</td>

</tr>

))

}


</tbody>

</table>

</section>

</>

)

}

export default ScanHistory;
