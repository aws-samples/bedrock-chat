import React, { useState, useEffect } from 'react';
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
  useEffect(() => {
    const setInitialPageState = async (_username: string) => {
        setUsername(_username);

        // LTI session info is passed in as query params. Extract and save state. 
        const queryParams = new URLSearchParams(location.search);
        const queryParamsObject: { [key: string]: string } = {};
        queryParams.forEach((value, key) => {
          queryParamsObject[key] = value;
        });
        //console.log('queryParamsObject', queryParamsObject);
        setLtiSession(queryParamsObject);
        const _email = queryParamsObject?.email;

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

  }, [location]);


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
      console.log(`login with *${ltiSession.email}*`);

      const {nextStep} = await signIn({
        username: ltiSession.email,
        options: {
          authFlowType: 'CUSTOM_WITHOUT_SRP'
        }
      });
      if (nextStep?.signInStep === 'CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE') {
        const user = await confirmSignIn({challengeResponse: 'opensesame'});
        console.log('Confirm response', user);
        goHome();
      } else {
        setPageState(PageState.ERROR);

      }
    } catch (err) {
      console.log('error = ', JSON.stringify(err));
      setPageState(PageState.ERROR);
    }
  }

  //
  // Render logic for the component 
  // 

  // set message based on pageState 
  const NextStep = {
    [PageState.LOADING]: { message: "Loading state. This screen should only be visible for 1-2 seconds.", action: null },
    [PageState.ERROR]: { message: "Something went wrong !!", action: null },
    [PageState.CONFIRM]: { message: `You are already logged in Qikr chat with ${username}. This request will switch your session to user ${ltiSession?.email}. Do you want to proceed ?`, action: () => startSignIn(true) },
    [PageState.LOGGING_IN]: { message: `Logging in as ${ltiSession?.email}` , action: () => startSignIn(false) },
    [PageState.REDIRECTING]: { message: "Logged in. Redirecting to the main app.", action: goHome }
  };
  const nextStep = NextStep[pageState];

  /*
  if (pageState === PageState.REDIRECTING) {
    console.log('Redirecting to home page');
    goHome();
  }
  if (pageState === PageState.LOGGING_IN) {
    console.log('Proceeding to log in directly');
    startSignIn(false);
  }
  */

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