import logo from './logo.svg';
import React, {useEffect} from "react";
import './App.css';
import Login from "./components/Login";
import Landing from "./components/Landing";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Logout from "./components/Logout";
import Register from "./components/Register";
import ChangePassword from "./components/ChangePassword";
import TagManager from 'react-gtm-module';

export const access_token_context = React.createContext("")

function App() {
    useEffect(() => {
       const tagManagerArgs = {
           gtmId: 'GTM-N4PXHKM9'
       };
       TagManager.initialize(tagManagerArgs);
    }, []);
    const [access_token, setToken] = React.useState("")
    return (
        <access_token_context.Provider value={{access_token, setToken}}>
            <Router>
                <Routes>
                    <Route path="/" Component={Login} />
                    <Route path='/landing' element={<ProtectedRoute><Landing /></ProtectedRoute>} /> //use element instead of component
                    <Route path='/logout' element={<ProtectedRoute><Logout /></ProtectedRoute>} />
                    <Route path="/register" Component={Register} />
                    <Route path="/change-password" Component={ChangePassword} />
                </Routes>
            </Router>
        </access_token_context.Provider>
    // <div className="App">
    //   <header className="App-header">
    //     <img src={logo} className="App-logo" alt="logo" />
    //     <p>
    //       Edit <code>src/App.js</code> and save to reload.
    //     </p>
    //     <a
    //       className="App-link"
    //       href="https://reactjs.org"
    //       target="_blank"
    //       rel="noopener noreferrer"
    //     >
    //       Learn React
    //     </a>
    //   </header>
    // </div>
    );
}

export default App;
