import React from 'react';
import { HashRouter as Router, Route } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import Home from '../routes/Home';
import PushupGuideLine from '../routes/pushup/guideLine';
import SquatGuideLine from '../routes/squat/guideLine';
import PushupExercise from '../routes/pushup/exercise';
import SquatExercise from '../routes/squat/exercise';
import Result from '../routes/Result';
import Login from '../routes/Login';
import Signup from '../routes/Signup';
import Statistics from '../routes/Statistics';
import Searching from '../routes/Searching';

// ()는 or 괄호 없는것 return 자동 / {}는 return 명시를 해줘야함
// path === link에서 to
export default () => (
    <Router>
        <Header/>
        <Route path='/' exact component={Home}/>
        <Route path='/login' exact component={Login}/>
        <Route path='/signup' exact component={Signup}/>
        <Route path='/pushup/guideLine' exact component={PushupGuideLine}/>
        <Route path='/squat/guideLine' exact component={SquatGuideLine}/>
        <Route path='/pushup/exercise' exact component={PushupExercise}/>
        <Route path='/squat/exercise' exact component={SquatExercise}/>
        <Route path='/Result' exact component={Result}/>
        <Route path='/statistics' exact component={Statistics}/>
        <Route path='/searching' exact component={Searching}/>
        <Footer/>
    </Router>
);


