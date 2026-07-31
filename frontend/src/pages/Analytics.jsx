// // Analytics page for phishing trends and aggregate model outcomes.
// import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
// import MetricCard from "../components/MetricCard.jsx";
// import PageHeader from "../components/PageHeader.jsx";

// const riskData = [
//   { risk: "Low", count: 0 },
//   { risk: "Medium", count: 0 },
//   { risk: "High", count: 0 },
// ];

// function Analytics() {
//   return (
//     <>
//       <PageHeader title="Analytics" description="Track detection volume, risk levels, and phishing trends." />
//       <div className="stats-grid">
//         <MetricCard label="Safe URLs" value="0" />
//         <MetricCard label="Suspicious URLs" value="0" />
//         <MetricCard label="Phishing URLs" value="0" />
//         <MetricCard label="Critical Events" value="0" />
//       </div>
//       <section className="card" style={{ marginTop: 18, height: 340 }}>
//         <h2>Risk Distribution</h2>
//         <ResponsiveContainer width="100%" height="82%">
//           <BarChart data={riskData}>
//             <CartesianGrid strokeDasharray="3 3" />
//             <XAxis dataKey="risk" />
//             <YAxis allowDecimals={false} />
//             <Tooltip />
//             <Bar dataKey="count" fill="#1769e0" radius={[6, 6, 0, 0]} />
//           </BarChart>
//         </ResponsiveContainer>
//       </section>
//     </>
//   );
// }

// export default Analytics;


// import { useEffect, useState } from "react";
// import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
// import MetricCard from "../components/MetricCard.jsx";
// import PageHeader from "../components/PageHeader.jsx";


// function Analytics() {

//   const [data, setData] = useState({
//     total_scans:0,
//     safe_count:0,
//     suspicious_count:0,
//     phishing_count:0,
//     critical_count:0
//   });


//   useEffect(()=>{

//     fetch("http://127.0.0.1:8000/api/analytics/summary")
//     .then(res=>res.json())
//     .then(result=>{
//         setData(result);
//     })
//     .catch(err=>console.log(err));

//   },[]);



// const riskData = [
//   { risk:"Low", count:data.safe_count },
//   { risk:"Medium", count:data.suspicious_count },
//   { risk:"High", count:data.phishing_count },
// ];


// return (
// <>
// <PageHeader 
// title="Analytics" 
// description="Track detection volume, risk levels, and phishing trends."
// />


// <div className="stats-grid">

// <MetricCard 
// label="Safe URLs" 
// value={data.safe_count}
// />

// <MetricCard 
// label="Suspicious URLs" 
// value={data.suspicious_count}
// />

// <MetricCard 
// label="Phishing URLs" 
// value={data.phishing_count}
// />

// <MetricCard 
// label="Critical Events" 
// value={data.critical_count}
// />

// </div>


// <section className="card" style={{marginTop:18,height:340}}>

// <h2>Risk Distribution</h2>

// <ResponsiveContainer width="100%" height="82%">

// <BarChart data={riskData}>

// <CartesianGrid strokeDasharray="3 3"/>

// <XAxis dataKey="risk"/>

// <YAxis allowDecimals={false}/>

// <Tooltip/>

// <Bar 
// dataKey="count"
// fill="#1769e0"
// />

// </BarChart>

// </ResponsiveContainer>

// </section>

// </>
// )

// }


// export default Analytics;

// import {
// Bar,
// BarChart,
// CartesianGrid,
// ResponsiveContainer,
// Tooltip,
// XAxis,
// YAxis
// }
// from "recharts";

// import MetricCard from "../components/MetricCard.jsx";
// import PageHeader from "../components/PageHeader.jsx";


// const riskData=[

// {
// risk:"No Risk",
// count:35
// },

// {
// risk:"Medium Risk",
// count:0
// },

// {
// risk:"High Risk",
// count:9
// }

// ];



// function Analytics(){


// return (

// <>


// <PageHeader

// title="Analytics"

// description="Track detection volume, risk levels, and phishing trends."

// />




// <div className="stats-grid">


// <MetricCard
// label="Safe URLs"
// value="35"
// />


// <MetricCard
// label="Suspicious URLs"
// value="0"
// />


// <MetricCard
// label="Phishing URLs"
// value="9"
// />


// <MetricCard
// label="Critical Events"
// value="7"
// />


// </div>



// <section
// className="card"
// style={{marginTop:18,height:340}}
// >


// <h2>
// Risk Distribution
// </h2>



// <ResponsiveContainer
// width="100%"
// height="82%"
// >


// <BarChart data={riskData}>


// <CartesianGrid strokeDasharray="3 3"/>


// <XAxis dataKey="risk"/>


// <YAxis allowDecimals={false}/>


// <Tooltip/>


// <Bar
// dataKey="count"
// fill="#1769e0"
// radius={[6,6,0,0]}
// />


// </BarChart>


// </ResponsiveContainer>


// </section>



// </>

// )

// }


// export default Analytics;
import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import MetricCard from "../components/MetricCard.jsx";
import PageHeader from "../components/PageHeader.jsx";

function Analytics() {
  const [data, setData] = useState({
    safe_count: 0,
    suspicious_count: 0,
    phishing_count: 0,
    critical_count: 0,
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/analytics/summary")
      .then((res) => res.json())
      .then((result) => setData(result))
      .catch((err) => console.error(err));
  }, []);

  const riskData = [
    {
      risk: "No Risk",
      count: data.safe_count
    },
    {
      risk: "Medium Risk",
      count: data.suspicious_count
    },
    {
      risk: "High Risk",
      count: data.phishing_count
    }
  ];

  return (
    <>
      <PageHeader
        title="Analytics"
        description="Track detection volume, risk levels, and phishing trends."
      />

      <div className="stats-grid">
        <MetricCard
          label="Safe URLs"
          value={data.safe_count}
        />

        <MetricCard
          label="Suspicious URLs"
          value={data.suspicious_count}
        />

        <MetricCard
          label="Phishing URLs"
          value={data.phishing_count}
        />

        <MetricCard
          label="Critical Events"
          value={data.critical_count}
        />
      </div>

      <section
        className="card"
        style={{ marginTop: 18, height: 340 }}
      >
        <h2>Risk Distribution</h2>

        <ResponsiveContainer
          width="100%"
          height="82%"
        >
          <BarChart data={riskData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="risk" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar
              dataKey="count"
              fill="#1769e0"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </section>
    </>
  );
}

export default Analytics;