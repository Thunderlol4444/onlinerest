import React, {useContext, useEffect} from 'react';
import {access_token_context} from "../App";
import "../App.css"
import {
    Button, Input, Text,
} from "@chakra-ui/react";
import {Navigate} from "react-router-dom";
import Ais from './Ais'


export default function Landing() {
    const [logout, setLogout] = React.useState(false);
    const { access_token, setToken } = useContext(access_token_context);
    const [datas, setDatas] = React.useState([]);

    const [isPopupOpen, setIsPopupOpen] = React.useState(false);
    const openPopup = () => {
    setIsPopupOpen(true);
    };

    const closePopup = () => {
    setIsPopupOpen(false);
    }

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (token) {
            setToken(token);
        }

        if (access_token !== '') {
            const getdata = async () => {
                const response = await fetch("https://onlinerest-1022384984816.asia-southeast1.run.app/getusers", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`,
                    },
                })
                setDatas(await response.json());
            }
            getdata()
        }
    },[]);

    function DataTable(){
        if (datas !== []) {
            try {
                return datas.map(function (item) {
                    return (
                        <tbody>
                            <tr>
                                <th className="th">{item[2]}</th>
                                <th className="th">{item[3]}</th>
                                <th className="th">{item[0]}</th>
                                <th className="th">{item[1]}</th>
                            </tr>
                        </tbody>)
                })
            }
            catch (err){
                console.log(err)
            }
        }
        }



    function Redirect(){
        if (logout) {
            return <Navigate to="/logout" replace={true}/>
        }
    }
    return(
        <>
            <div className="logout">
                <Button onClick={openPopup} size='small' fontSize="0.2em" colorScheme="#3498db" top="1vh" color="#666666">jan</Button>
                {isPopupOpen && <Popup onClose={closePopup}/>}
                <Button className='logout-button' colorScheme="red" size="sm" onClick={setLogout}>Logout</Button>
                <Redirect/>
                <div className="table-layout">
                    <table className="data-table">
                        <thead className="thead">
                        <tr className="tr">
                            <th className="th1">Id</th>
                            <th className="th1">Name</th>
                            <th className="th1">Email</th>
                            <th className="th1">Password</th>
                        </tr>
                        </thead>
                        <DataTable/>
                    </table>
                </div>
                <Ais/>
            </div>
        </>

    )
}

export const Popup = ({onClose}) => {
    const [pwd, setpwd] = React.useState("");
    const handlepwd = (e) => {
        const {value} = e.target
        setpwd(value);
    }

    return (
        <div className="popup-container">
            <div className="popup">
                {pwd === "1025" && <Text color="black" align="center">I love you dear</Text>}
                <br/>
                <Input placeholder="pwd" size="xs" width="auto" value={pwd} onChange={handlepwd}
                       color="black" mb="5"></Input>
                <br/>
                <Button onClick={onClose} color="black">Close</Button>
            </div>
        </div>
    )
}
