import {Icon} from 'leaflet'

const legalIcon = new Icon ({
    iconUrl : 'https://img.icons8.com/external-icongeek26-linear-colour-icongeek26/64/external-legal-business-and-finance-icongeek26-linear-colour-icongeek26.png',
    iconSize : [35,35], // size of the icon
    iconAnchor : [22,94], // point of the icon which will correspond to marker's location
    popupAnchor : [-3, -76] // point from which the popup should open relative to the iconAnchor

})
const foodIcon = new Icon ({
    iconUrl : 'https://img.icons8.com/doodle/48/apple.png',
    iconSize : [35, 35], // size of the icon
    iconAnchor : [22, 94], // point of the icon which will correspond to marker's location
    popupAnchor : [-3, -76] // point from which the popup should open relative to the iconAnchor
})
const healthIcon = new Icon ({
    iconUrl: 'https://img.icons8.com/doodle/48/heart-with-pulse.png',
    iconSize : [35,35], // size of the icon
    iconAnchor : [22,94], // point of the icon which will correspond to marker's location
    popupAnchor : [-3, -76] // point from which the popup should open relative to the iconAnchor
})

const shipIcon = new Icon({
    iconUrl: 'https://img.icons8.com/ios/100/battleship-top-view.png',
    iconSize: [38, 45], // size of the icon
    iconAnchor: [0, 0], // point of the icon which will correspond to marker's location
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
})

export { legalIcon, foodIcon, healthIcon, shipIcon}