import Router from './Router';
import GlobalStyles from "./GlobalStyles";
import '../index.css';

export default function App(){
    return(
        <>
            <GlobalStyles />
            <Router>
                <div className="App"></div>
            </Router>
        </>
    )
}