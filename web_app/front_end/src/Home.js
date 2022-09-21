import YouTube from 'react-youtube';
import { Container, Row, Col, Button } from 'react-bootstrap';

function Home(props) {
  const opts = {
    height: '390',
    width: '640',
    playerVars: {
      // https://developers.google.com/youtube/player_parameters
      autoplay: 1,
    },
  };

  const _onReady = (event) => {
    // access to player in all event handlers via event.target
    event.target.playVideo();
  }

  return (
          <div>
          <p>home</p>
          <YouTube videoId="2g811Eo7K8U" opts={opts} onReady={_onReady} />
          <Button onClick={() => props.setView(1)}>start</Button>
          </div>
  );
}

export default Home;