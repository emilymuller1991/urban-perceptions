import { useState } from "react";
import { v4 as uuidv4 } from 'uuid';
import { Container, Row, Col, Button } from 'react-bootstrap';
import Contact from "./Contact"
import Home from "./Home"

function Images(props) {
  const host = process.env.REACT_APP_BACK_END_HOST;
  const port = process.env.REACT_APP_BACK_END_PORT;
  const [api, setApi] = useState(process.env.REACT_APP_API_KEY);

  const [cache, setCache] = useState(0);
  const [userId, setUserId] = useState(uuidv4());

  const date = () => {
    return String(Intl.DateTimeFormat('en-US', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(Date.now()))
  }

  const submit = (img_1, img_2, perception, choice, user_id) => {
    const requestOptions = {
      method: 'POST',
      header: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://' + host + ':5000/post_data', 'Accept': 'application/json' },
      mode: 'cors',
      body: JSON.stringify(
        {
          "img_1": img_1,
          "img_2": img_2,
          "perception": perception,
          "choice": choice,
          "user_id": user_id,
          "time": date()
        }
      )
    };
    fetch('http://' + host + ':5000/post_data', requestOptions)
      .then(response => response.json())
  };

  // render image using API
  const img_html = (panoid, head) => {
    var heady = Math.round(head);
    return `https://maps.googleapis.com/maps/api/streetview?size=640x640&pano=${panoid}&fov=120&heading=${heady}&pitch=0&key=${api}`
  };

  const updates = () => {
    // count the image pairs to refresh data bindings
    setCache(cache + 2);
    if ((cache + 2) % 10 === 0) {
        props.fetchImage();
        setCache(0);
    }
};

  return (
    <div className="App">
      <p>Images</p>
      {console.log(props.meta)}
      <Row className='page'>
                <div class="col-lg-4 offset-lg-1 col-md-4 offset-md-1 p-1">
                    <img className='images' onClick={() => { submit(props.meta.meta[cache].idx, props.meta.meta[cache + 1].idx, 'choice', props.meta.meta[cache].idx, userId); updates() }} src={img_html(props.meta.meta[cache].panoid, props.meta.meta[cache].head)} alt='image not loaded' />
                </div>
                <div class="col-lg-2 offset-lg-0 col-md-2 offset-md-0">
                    <Button variant="outline-secondary" className='button' size='lg' block onClick={() => { submit(props.meta.meta[cache][2], props.meta.meta[cache + 1][2], 'choice', '1', userId); updates() }}>≈ Roughly Equal</Button>
                    <Button variant="outline-secondary" className='button' size='lg' block onClick={() => { submit(props.meta.meta[cache][2], props.meta.meta[cache + 1][2], 'choice', '0', userId); updates() }}>x Not Comparable</Button>
                    <Button variant="outline-secondary" className='button' size='lg' block onClick={() => { submit(props.meta.meta[cache][2], props.meta.meta[cache + 1][2], 'choice', '2', userId); updates() }}>Image not shown</Button>
                </div>
                
                <div class="col-lg-4 offset-lg-0 col-md-4 p-1">
                    <img className='images' onClick={() => { submit(props.meta.meta[cache].idx, props.meta.meta[cache + 1].idx, 'choice', props.meta.meta[cache + 1].idx, userId); updates() }} src={img_html(props.meta.meta[cache + 1].panoid, props.meta.meta[cache + 1].head)} alt='image not loaded' />
                </div>
            </Row>
    </div>
  );
}
export default Images;
