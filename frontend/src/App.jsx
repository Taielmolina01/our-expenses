import './App.css'
import { Route, Routes } from 'react-router-dom';
import { ApplySavedTheme } from './utils';
import LandingPage from './pages/landingPage'
import SignIn from './pages/signIn';
import SignUp from './pages/signUp'
import Home from './pages/home'
import Group from './pages/group';
import User from './pages/user';
import PrivateRoute from './PrivateRoute';

function App() {
  ApplySavedTheme();
  return (
    <>
      <Routes>
          <Route index element={<LandingPage />}/>
          <Route path="/sign-in" element={<SignIn />}/>
          <Route path="/sign-up" element={<SignUp />}/>
          <Route
            path="/home"
            element={
              <PrivateRoute>
                <Home />
              </PrivateRoute>
            }
          />
          <Route
            path="/groups/:groupID/:groupName"
            element={
              <PrivateRoute>
                <Group />
              </PrivateRoute>
            }
          />
          <Route
            path="/users/:userEmail"
            element={
              <PrivateRoute>
                <User />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<LandingPage />} /> 
      </Routes>
    </>
  )
}

export default App;
