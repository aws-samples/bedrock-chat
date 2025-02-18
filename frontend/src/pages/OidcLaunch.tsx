import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate} from 'react-router-dom';
import { getCurrentUser} from 'aws-amplify/auth';

import {signOut, signIn, confirmSignIn} from 'aws-amplify/auth';


const OidcLaunch: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const [ltiSession, setLtiSession] = React.useState<any>(null);
  // We will likely need to move ltiSession to the App so other child component can access the state. 
  //   alternatively we can store the session state in local strage and other componetnes can read it from there.

  const [username, setUsername] = useState('');
  const [pageState, setPageState] = useState('loading');
  // State moves through the following states in sequence except for the error state that can be reached at any time
  // loading    : parse query params and get user sesion from local storage
  // check_id   : state fetched. Prompt user if the user session is going to switch 
  // start_auth : initiate auth with Cognito 
  // done       : probably won't use this state. Instead we will directly navigate to main page. 
  // error      : in case something goes wrong 
  // 
  // On succesful authetnication, we will navigate to the main page. Succesful authentication can happen under 2 conditions : 
  //   1. in 'check_id' state when we discover that we are already logged in 
  //   2. succesful authenticaiton during 'confirm' state
  //

  // Run this effect only once when the component is mounted
  
  useEffect(() => {
    // check if we have an active user session
    getCurrentUser()
        .then(user => {
            console.log("User = ", user);
            setUsername(user?.signInDetails?.loginId || '');
        })
        .catch(() => {
            console.log("No session active");
        })

    // Parse query params that include LTI params from Canvas 
    const queryParams = new URLSearchParams(location.search);
    const queryParamsObject: { [key: string]: string } = {};
    queryParams.forEach((value, key) => {
      queryParamsObject[key] = value;
    });
    console.log('queryParamsObject', queryParamsObject);
    setLtiSession(queryParamsObject);
    if (ltiSession?.email === null) {
      setPageState('error');
    } else {
      setPageState('check_id');
    }
  }, [location]);


  const goHome = () => {
    console.log('go home final ?? navigate and reload ');
    //window.location.href = "/"
    navigate('/');
    window.location.reload();
  }

  const startSignIn = async (userSignedIn: boolean) => {
    try {
      console.log('current user = ', username);

      if (userSignedIn === true) {
        await signOut();
      }
      console.log(`login with *${ltiSession.email}*`);

      const {isSignedIn, nextStep} = await signIn({
        username: ltiSession.email,
        options: {
          authFlowType: 'CUSTOM_WITHOUT_SRP'
        }
      });
      console.log('signIn response :', isSignedIn, nextStep);
      console.log('... ', nextStep?.signInStep);
      if (nextStep?.signInStep === 'CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE') {
        console.log('Got challenge ', nextStep?.additionalInfo);
        const user = await confirmSignIn({challengeResponse: 'opensesame'});
        console.log('Confirm response', user);
        goHome();
      } else {
        setPageState('error');

      }
    } catch (err) {
      console.log('error = ', JSON.stringify(err));
      alert('Incorrect username or password');
      setPageState('error');
    }
  }

  if (pageState === 'loading') {
    console.log('Loading state');
    return <div>Loading state. This screen should only be visible for 1-2 seconds.  </div>;
  }

  if (pageState === 'error') {
    console.log('error -- lti session', ltiSession);
    return <div>Something went wrong !! </div>;
  }

  if (pageState === 'check_id') {
    console.log('lti session = ', ltiSession);   // TODO remove debug print

    // Already logged in. Launch the app
    if (ltiSession.email === username) {
      console.log(`User already logged in as ${ltiSession.email}. Forward to the main app`);
      return (<div> 
        <div> You are already logged in as {ltiSession.email}. We will reuse the current sesion. </div> 
        <button onClick={() => goHome()} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Continue
        </button>
      </div>)
    }

    // Not logged in. Start auth
    if (username === '') {
      console.log('No session. We will now create a new session.');
      //startSignIn();
      return (<div> 
        <div> No session. We will now create a new session. </div> 
        <button onClick={() => startSignIn(false)} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Continue
        </button>
      </div>)
      return <div>Logging in as {ltiSession.email}</div>;
    }

    // Logged in with different user. Check with user before logging in.
    return (<div> 
      <div> You are already logged in Qikr chat with {username}. </div> 
      <div> This request will switch your session to user {ltiSession.email}. </div>
      <div> Do you want to proceed ? </div>
      <button onClick={() => startSignIn(true)} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
        Yes
      </button>
    </div>)
  }
  return <div> Should not happen </div>;



};

export default OidcLaunch;