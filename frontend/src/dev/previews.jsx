import {ComponentPreview, Previews} from '@react-buddy/ide-toolbox'
import {PaletteTree} from './palette'
import Ais from "../components/Ais";

const ComponentPreviews = () => {
    return (
        <Previews palette={<PaletteTree/>}>
            <ComponentPreview path="/Ais">
                <Ais/>
            </ComponentPreview>
        </Previews>
    )
}

export default ComponentPreviews