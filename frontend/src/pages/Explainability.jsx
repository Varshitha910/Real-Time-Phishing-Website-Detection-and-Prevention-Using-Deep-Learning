// // Explainability page for showing SHAP feature contributions.
// import PageHeader from "../components/PageHeader.jsx";

// const topFeatures = [
//   { feature: "url_length", impact: 0.0 },
//   { feature: "suspicious_keyword_count", impact: 0.0 },
//   { feature: "ip_address_present", impact: 0.0 },
// ];

// function Explainability() {
//   return (
//     <>
//       <PageHeader title="Explainability" description="Inspect the URL features that influence model predictions." />
//       <section className="card">
//         <h2>Top Feature Contributions</h2>
//         <table className="table">
//           <thead>
//             <tr>
//               <th>Feature</th>
//               <th>Impact</th>
//             </tr>
//           </thead>
//           <tbody>
//             {topFeatures.map((item) => (
//               <tr key={item.feature}>
//                 <td>{item.feature}</td>
//                 <td>{item.impact}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </section>
//     </>
//   );
// }

// export default Explainability;



// import {useEffect,useState} from "react";
// import PageHeader from "../components/PageHeader.jsx";


// function Explainability(){

// const [features,setFeatures]=useState([]);


// useEffect(()=>{


// fetch("http://127.0.0.1:8000/explain")
// .then(res=>res.json())
// .then(data=>{

// console.log(data);

// if(data.explanation){
// setFeatures(data.explanation);
// }

// })
// .catch(err=>console.log(err));


// },[]);



// return(
// <>

// <PageHeader
// title="Explainability"
// description="Inspect the URL features that influence model predictions."
// />


// <section className="card">


// <h2>Top Feature Contributions</h2>


// <table className="table">

// <thead>

// <tr>

// <th>Feature</th>
// <th>Impact</th>
// <th>Description</th>

// </tr>

// </thead>


// <tbody>


// {
// features.map((item,index)=>(

// <tr key={index}>

// <td>{item.feature}</td>

// <td>{item.impact}</td>

// <td>{item.description}</td>

// </tr>

// ))

// }


// </tbody>


// </table>


// </section>


// </>

// )

// }


// export default Explainability;
// import {useState} from "react";
// import PageHeader from "../components/PageHeader.jsx";


// function Explainability(){

// const [url,setUrl]=useState("");
// const [features,setFeatures]=useState([]);



// async function checkExplain(){


// const res = await fetch(
// "http://127.0.0.1:8000/api/explain",
// {
// method:"POST",
// headers:{
// "Content-Type":"application/json"
// },
// body:JSON.stringify({
// url:url
// })
// }
// );


// const data = await res.json();


// console.log(data);


// setFeatures(data.explanation || []);

// }



// return(
// <>

// <PageHeader
// title="Explainability"
// description="Inspect the URL features that influence model predictions."
// />


// <section className="card">


// <input
// placeholder="Enter URL"
// value={url}
// onChange={(e)=>setUrl(e.target.value)}
// />


// <button onClick={checkExplain}>
// Explain
// </button>



// <h2>Top Feature Contributions</h2>


// <table className="table">

// <thead>

// <tr>
// <th>Feature</th>
// <th>Impact</th>
// <th>Description</th>
// </tr>

// </thead>


// <tbody>

// {
// features.map((item,index)=>(

// <tr key={index}>

// <td>{item.feature}</td>

// <td>{item.impact}</td>

// <td>{item.description}</td>

// </tr>

// ))
// }


// </tbody>


// </table>


// </section>


// </>

// )

// }

// export default Explainability;

import {useState} from "react";
import PageHeader from "../components/PageHeader.jsx";


function Explainability(){

const [url,setUrl]=useState("");
const [features,setFeatures]=useState([]);


async function checkExplain(){


const detectResponse = await fetch(
"http://127.0.0.1:8000/api/detect",
{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
url:url,
source:"dashboard"
})
});


const detectData = await detectResponse.json();



const explainResponse = await fetch(
"http://127.0.0.1:8000/api/explain",
{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({

url:url,

features:detectData.features

})
});


const explainData = await explainResponse.json();


console.log(explainData);


// setFeatures(
// explainData.explanation || []
// );
setFeatures(
 explainData.top_contributions || []
);


}



return(
<>

<PageHeader
title="Explainability"
description="Inspect the URL features that influence model predictions."
/>


<section className="card">


<input
placeholder="Enter URL"
value={url}
onChange={(e)=>setUrl(e.target.value)}
/>


<button onClick={checkExplain}>
Explain
</button>



<h2>Top Feature Contributions</h2>


<table className="table">

<thead>

<tr>
<th>Feature</th>
<th>Impact</th>
<th>Description</th>
</tr>

</thead>


<tbody>

{
features.map((item,index)=>(

<tr key={index}>

<td>{item.feature}</td>

<td>{item.impact}</td>

<td>{item.description}</td>

</tr>

))
}

</tbody>


</table>


</section>

</>
)

}


export default Explainability;