import {useState} from "react";
import Contact from "./Contact"
import Images from "./Images"
import Home from "./Home"
import "./App.css";
require('dotenv').config({path: '../.env'});

function App() {

  const [view, setView] = useState(2);
  const [meta, setMeta] = useState({ meta: 'aaa' });

  const host = process.env.REACT_APP_BACK_END_HOST;
  const port = process.env.REACT_APP_BACK_END_PORT;


  const fetchImage = () => {
    const requestOptions = {
      method: 'GET',
      header: { 'Content-Type': 'application/json'}
    };
    fetch('http://' + host + ':' + port + '/get_data', requestOptions)
      .then(response => response.json())
      .then(result => {
        setMeta({
          meta: result.map(item => ({
            panoid: item[0],
            month: item[1],
            idx: item[2],
            angle: item[3],
            head: item[4],
            cluster: item[5],
            pp: item[6],
            pp_float: item[8]
          }))
        });
      });
  };

  return (
    <div className="App">
      <p>perceptions</p>
      <button onClick={() => setView(0)}>contactInfo</button>
      <button onClick={() => { setView(1); fetchImage() }}>images</button>
      <button onClick={() => setView(2)}>home</button>
      { view === 0 ? <Contact/> : null}
      { view === 1 ? <Images setView={setView} fetchImage={fetchImage} meta={meta} /> : null}
      { view === 2 ? <Home setView={setView}/> : null}
    </div>
  );
}
export default App;
