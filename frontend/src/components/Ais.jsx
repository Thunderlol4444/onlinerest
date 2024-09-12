import React, {useEffect} from 'react';
import "../App.css"
import { MapContainer, TileLayer, Marker, Popup} from "react-leaflet";
import 'leaflet/dist/leaflet.css';
import {shipIcon} from "./Icons";
import {vesselType, status, manoeuverIndicator, positionAccuracy, RAIMFlag, checkHeading} from "./AisCode";
import 'leaflet-rotatedmarker'

export default function Ais() {
    const [responseData, setData] = React.useState([]);
    // async function ais_data(){
    //     const data = await fetch("http://localhost:8000/ais_data",{
    //         method: "get",
    //         headers: {
    //             "Authorization": `Bearer ${localStorage.getItem("access_token")}`,},
    //     })
    //     setData(await data.json());
    //     // console.log(responseData);
    // }


    async function ais_data_A(){
        const data = await fetch("http://localhost:8000/ais_data_A",{
            method: "get",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,},
        }).then()
        setData(await data.json());
        console.log(responseData);
    }


    useEffect(() => {
        //ais_data()
        ais_data_A()

    }, []);

    // var vesselCoordinates = responseData.map(function (item) {
    //     return({name: item[0], latitude: item[3], longitude: item[4]});
    // })
    // const vesselDetails = responseData.map(function(item){
    //     return ({contact_number: item[1], time: item[2], latitude: item[3], longitude: item[4],
    //         speed_over_ground: item[5], course_over_ground: item[6], heading: item[7], name: item[8],
    //         international_maritime_organisation: item[9], callsign: item[10], type: vesselType(item[11]),
    //         status: status(item[12]), length: item[13], width: item[14], draft: item[15], cargo: vesselType(item[16]),
    //         transceiver: item[17]});
    // })
    // console.log(vesselDetails)

    const vesselDetails = responseData.map(function (item){
        return ({message_type: item[1], repeat_indicator: item[2], MMSI: item[3], navigation_status: status(item[4]),
                rate_of_turn: item[5], speed_over_ground: item[6], position_accuracy: positionAccuracy(item[7]),
                longitude: item[8], latitude: item[9], course_over_ground: item[10], true_heading: checkHeading(item[11]),
                time_stamp: item[12], manoeuver_indicator: manoeuverIndicator(item[13]), spare: item[14],
                RAIM_flag: RAIMFlag(item[15]), radio_status: item[16]
        });
    })


    return (
        <div className="map-container">
            <MapContainer center={[40.6462288, -73.95754575]} zoom={14} style={{height: '700px', width: '100%'}}>
                <TileLayer url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png'/>
                           {/*{attribution = "© OpenStreetMap contributors"}/>*/}
                {vesselDetails.map((vessel, index) => (
                    <Marker
                        key={index}
                        position={[vessel.latitude, vessel.longitude]}
                        icon={shipIcon}
                        rotationAngle={Number(vessel.true_heading)-45}
                    >
                        <Popup>
                            <b>Time stamp: {vessel.time_stamp} seconds</b><br/>
                            <b>Message type: {vessel.message_type}</b><br/>
                            <b>Navigation status: {vessel.repeat_indicator}</b><br/>
                            <b>Rate of turn: {vessel.rate_of_turn} degrees/min</b><br/>
                            <b>Speed over ground: {vessel.speed_over_ground} knots</b><br/>
                            <b>Position accuracy: {vessel.repeat_indicator}</b><br/>
                            <b>Longitude: {vessel.longitude} degrees</b><br/>
                            <b>Latitude: {vessel.latitude} degrees</b><br/>
                            <b>Course over ground: {vessel.course_over_ground} degrees</b><br/>
                            <b>True heading: {(vessel.true_heading)} degrees</b><br/>
                            <b>Manoeuver indicator: {vessel.manoeuver_indicator}</b><br/>
                            <b>RAIM flag: {vessel.RAIM_flag}</b><br/>
                            <b>Radio status: {vessel.radio_status}</b><br/>
                            <em>MMSI: {vessel.MMSI}</em>
                            {/*<b>Time: {vessel.time.slice(0,10)+' '+vessel.time.substring(11)}</b><br/>*/}
                            {/*<b>Name: {vessel.name}</b><br/>*/}
                            {/*<b>SOG: {vessel.speed_over_ground} knots</b><br/>*/}
                            {/*<b>COG: {vessel.course_over_ground} degrees</b><br/>*/}
                            {/*<b>Heading: {vessel.heading} degrees</b><br/>*/}
                            {/*<b>IMO: {vessel.international_maritime_organisation}</b><br/>*/}
                            {/*<b>Callsign: {vessel.callsign}</b><br/>*/}
                            {/*<b>Length: {vessel.length} meters</b><br/>*/}
                            {/*<b>Width: {vessel.width} meters</b><br/>*/}
                            {/*<b>Draft: {vessel.draft} meters</b><br/> /!*draft depth of vessel*!/*/}
                            {/*<b>Type: {vessel.type}</b><br/>*/}
                            {/*<b>Status: {vessel.status}</b><br/>*/}
                            {/*<b>Cargo: {vessel.cargo}</b><br/>*/}
                            {/*<b>Transceiver: {vessel.transceiver}</b><br/>*/}
                            {/*<em>Contact Number: {vessel.contact_number}</em><br/> /!*Maritime Mobile Service identity value*!/*/}
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>
        </div>
    )
}