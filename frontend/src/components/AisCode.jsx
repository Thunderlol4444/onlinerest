function status(data){
    switch(data){
        case 0:
            return "Under way using engine"
        case 1:
            return "At anchor"
        case 2:
            return "Not under command"
        case 3:
            return "Restricted manoeuverbility"
        case 4:
            return "Constrainted by her draught"
        case 5:
            return "Moored"
        case 6:
            return "Aground"
        case 7:
            return "Engaged in Fishing"
        case 8:
            return "Under way sailing"
        case 9:
            return "Reserved for future amendment of Navigational Status of HSC"
        case 10:
            return "Reserved for future amendment of Navigational Status of WIG"
        case 11:
            return "Reserved for future use"
        case 12:
            return "Reserved for future use"
        case 13:
            return "Reserved for future use"
        case 14:
            return "AIS-SART is active"
        case 15:
            return "Not defined"
    }
}

function vesselType(vesseltype){
    switch (vesseltype){
        case 0:
            return "Not available"
        case vesseltype>=1 && vesseltype<=19:
            return "Reserved for future use"
        case vesseltype>=20 && vesseltype<=29:
            return "Wing in ground (WIG)"
        case 30:
            return "Fishing"
        case 31:
            return "Towing"
        case 32:
            return "Towing: Length exceeds 200m or breath exceeds 25m"
        case 33:
            return "Dredging or underwater operations"
        case 34:
            return "Diving operations"
        case 35:
            return "Military operations"
        case 36:
            return "Sailing"
        case 37:
            return "Pleasure Craft"
        case 38:
            return "Reserved"
        case 39:
            return "Reserved"
        case vesseltype>=40 && vesseltype<=49:
            return "High speed craft"
        case 50:
            return "Pilot Vessel"
        case 51:
            return "Search and Rescue Vessel"
        case 52:
            return "Tug"
        case 53:
            return "Port Tender"
        case 54:
            return "Anti-pollution equipment"
        case 55:
            return "Law Enforcement"
        case vesseltype>= 56 && vesseltype<=57:
            return "Spare - for assignment to local vessel"
        case 58:
            return "Medical Transport"
        case 59:
            return "Ship according to RR Resolution No.18"
        case vesseltype>=60 && vesseltype<=69:
            return "Passenger"
        case vesseltype>=70 && vesseltype<=79:
            return "Cargo"
        case vesseltype>=80 && vesseltype<=89:
            return "Tanker"
        case vesseltype>=90 && vesseltype<=99:
            return "Other"
    }
}


function manoeuverIndicator(manoever_indicator){
    switch (manoever_indicator){
        case 0:
            return "Not available"
        case 1:
            return "No special manoeuver"
        case 2:
            return "Special manoeuver"
    }
}


function positionAccuracy(position_accuracy){
    switch (position_accuracy){
        case 0:
            return "> 10m"
        case 1:
            return "<>> 10m"
    }
}

function RAIMFlag(RAIMflag){
    switch (RAIMflag){
        case 0:
            return "RAIM not in use"
        case 1:
            return "RAIM in use"
    }
}

function checkHeading(heading){
    if (heading === 511){
        return "N/A"
    }return heading
}


function CSUnit(cs_unit){
    switch (cs_unit){
        case 0:
            return "Class B SOTDMA"
        case 1:
            return "Class B Carrier Sense"
    }
}


function displayFlag(display_flag){
    switch (display_flag){
        case 0:
            return "No visual display"
        case 1:
            return "Has display (Probably not reliable)"
    }
}


function checkAvailability(availability){
    switch (availability){
        case 0:
            return "N/A"
        case 1:
            return "Available"
    }
}


function assigned(assigned_mode){
    switch (assigned_mode){
        case 0:
            return "Autonomous mode"
        case 1:
            return "Assigned mode"
    }
}
module.exports = {vesselType, status, manoeuverIndicator, positionAccuracy, RAIMFlag, checkHeading, CSUnit, displayFlag,
                    checkAvailability, assigned}