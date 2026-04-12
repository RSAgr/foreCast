import './App.css'
import {WavyBackground} from './components/ui/wavy-background'

function App() {

  return(
    <>
    <WavyBackground className="max-w-4xl mx-auto pb-40">
      <p className="text-2xl md:text-4xl lg:text-7xl text-white font-bold inter-var text-center">
        Forecast 
      </p>
      <p className="text-base md:text-lg mt-4 text-white font-normal inter-var text-center">
        Answer to your questions about the future, powered by AI. Ask anything, and get insights that help you make informed decisions.
      </p>
    </WavyBackground>
    </>
  )
}

export default App
