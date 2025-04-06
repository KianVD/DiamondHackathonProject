import logo from './logo.svg';
import './App.css';
import FileUploadLanding from './FileUpload';
import LogoutButton from './Logout';

function App() {
  return (
    <div className="App">
           <LogoutButton />
            <img src="./thumbnail.png" alt="Thumbnail" className="thumbnail" />
     <FileUploadLanding />
     <LogoutButton />
    </div>
  );
}

export default App;
