import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate} from 'react-router-dom';
import { getCurrentUser} from 'aws-amplify/auth';
import {signOut, signIn, confirmSignIn} from 'aws-amplify/auth';


const LtiLaunch: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // ltiSession tracks information for the current LTI session.
  // We will likely need to move ltiSession further up in the component hierarchy,
  // so other child components can access the state. Alternatively, we can store
  // the session state in local storage and other components can read it from there.
  const [ltiSession, setLtiSession] = React.useState<any>(null);

  // username is the email id for the user currently logged in
  const [username, setUsername] = useState<string>('');


  enum PageState {
    LOADING = 'LOADING',
    CONFIRM = 'CONFIRM',
    LOGGING_IN = 'LOGGING_IN',
    REDIRECTING = 'REDIRECTING',
    ERROR = 'ERROR'
  };
  const [pageState, setPageState] = useState<PageState>(PageState.LOADING);
  // pageState representes a state machine for LTI based authentication. 
  // LOADING : User will not see this screen in normal situations. 
  //           Initial state while we fetch user details from local storage. We transition to 
  //           other states based on the following tests. 
  //           If current session different from LTI session, go to CONFIRM state  
  //           If no current session, got to LOGGING_IN state
  //           If current session is same as LTI session, go to REDIRECTING state  
  // CONFIRM : Confirm with user if it is ok to switch login to the new user. This is only presented if
  //          we are currently logged in as a different user. After user confiration, state will transition to
  //          LOGGING_IN
  // LOGGING_IN : Initiate auth with Cognito. If necessary, log out the current user.
  // REDIRECTING : This state is presented briefly as we redirect. 
  // ERROR : In case something goes wrong in any of the operations. This can only be reached 
  //
  // On succesful authetnication, we will navigate to the main page. 


  // Run this effect only once when the component is mounted
  const alreadyRanOnce = useRef(false);
  useEffect(() => {
    const setInitialPageState = async (_username: string) => {
        setUsername(_username);
        if (alreadyRanOnce.current) return;
        alreadyRanOnce.current = true;

        // LTI session info is passed in as query params. Extract and save state. 
        const queryParams = new URLSearchParams(location.search);
        const queryParamsObject: { [key: string]: string } = {};
        queryParams.forEach((value, key) => {
          queryParamsObject[key] = value;
        });
        //console.log('queryParamsObject', queryParamsObject);
        setLtiSession(queryParamsObject);
        const _email = queryParamsObject?.email;

        // Store the query params in local storage 
        localStorage.setItem('ltiSession', JSON.stringify(queryParamsObject))
        // set individual keys for every query param
        if (queryParamsObject) {
          console.log('setting indiviudal keys')
          Object.keys(queryParamsObject).forEach((key) => {
            localStorage.setItem(key, queryParamsObject[key]);
          });
        }

        if (_email === null) {
          setPageState(PageState.ERROR);
        } else if (_username === '') {
          setPageState(PageState.LOGGING_IN);
        } else if (_email !== _username) {
          setPageState(PageState.CONFIRM);
        } else {
          setPageState(PageState.REDIRECTING);
        }
    }
    // check if we have an active user session
    getCurrentUser()
      .then(user => {
        const _username = user?.signInDetails?.loginId || '';
        setInitialPageState(_username);
      })
      .catch(() => {
        setInitialPageState('');
      });

  }, []);


  const goHome = () => {
    console.log('Navigating to home page');
    navigate('/');
    window.location.reload();
  }

  const startSignIn = async (logoutUser: boolean) => {
    try {
      if (logoutUser === true) {
        await signOut();
      }

      const {nextStep} = await signIn({
        username: ltiSession.email,
        options: {
          authFlowType: 'CUSTOM_WITHOUT_SRP'
        }
      });
      if (nextStep?.signInStep === 'CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE') {
        await confirmSignIn({challengeResponse: 'opensesame'});
        goHome();
      } else {
        setPageState(PageState.ERROR);

      }
    } catch (err) {
      console.log('error = ', JSON.stringify(err));
      setPageState(PageState.ERROR);
    }
  }

  // For REDIRECTING state, we will navigate to the main page after 1 second
  // For SIGNING_IN state, we will call startSignIn after 1 second
  useEffect(() => {
    let action = null;
    if (pageState === PageState.REDIRECTING) {
      action = goHome;
    } else if (pageState === PageState.LOGGING_IN) {
      action = () => startSignIn(false);
    }
    if (action === null) return;

    // schedule a call to nextStep.action after few seconds 
    console.log(`Waiting 3 seconds ..`);
    const timer = setTimeout(() => {
      action();
    }, 3000);
    return () => clearTimeout(timer);  // cancel if component unmounts
  }, [pageState, navigate]);


  //
  // Render logic for the component 
  // 

  // set message based on pageState 
  const NextStep = {
    [PageState.LOADING]: { message: "Loading state. This screen should only be visible for 1-2 seconds.", action: null },
    [PageState.ERROR]: { message: "Something went wrong !!", action: null },
    [PageState.CONFIRM]: { message: `You are already logged in Qikr chat with ${username}. This request will switch your session to user ${ltiSession?.email}. Do you want to proceed ?`, action: () => startSignIn(true) },
    [PageState.LOGGING_IN]: { message: `Logging in as ${ltiSession?.email}` , action: null },
    [PageState.REDIRECTING]: { message: `Logged in as ${ltiSession?.email}. Redirecting to the main app.`, action: null}
  };
  const nextStep = NextStep[pageState];
  console.log('pageState', pageState); 


  return (<div> 
    <div> {nextStep.message} </div> 
    {nextStep.action  && (
      <button onClick={nextStep.action} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
        Continue
      </button>
    )}
  </div>);

};

export default LtiLaunch;