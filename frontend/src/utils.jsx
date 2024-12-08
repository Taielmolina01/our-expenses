const BACK_URL = import.meta.env.VITE_BACK_LOCAL;

const MAX_NAME_LENGTH = 30;

const HandleSignIn = async(email, password, setIsLoading, setError, setUser, navigate) => {
    try {
        setIsLoading(true);
        const res = await fetch(`${BACK_URL}/login`, {
            method: "POST",
            body: new URLSearchParams({
                username: email,
                password: password,
            }),
            cache: "no-store",
        });

        const data = await res.json();
  
        if (!res.ok) {
            setError(data.detail)
        } else {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            setUser(data);
            navigate("/home"); 
        }
    } catch (error) {
        setError("Connection error: " + error);
        return;
    } finally {
        setIsLoading(false)
    }
}

const LogOut = async(setIsLoading, setError, navigate) => {
    try {
        setIsLoading(true);
        const res = await fetch(`${BACK_URL}/logout`, {
            method: "POST",
            cache: "no-store",
            headers: {
                "Authorization": `Bearer ${GetToken()}`,
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        });

        if (res.ok) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            localStorage.setItem('theme', document.documentElement.classList.contains('light-mode') ? 'dark' : 'dark');
            navigate("/");
        } else {
            setError("Error logging out");
        }
    } catch (error) {
        setError("Connection error logging out: " + error);
    } finally {
        setIsLoading(false);
    }
}

const EditUser = async(setError, userName, setUser) => {

    try {
        const user = GetUser();
        const res = await fetch(`${BACK_URL}/users/${user.email}`, {
            method: "PUT",
            cache: "no-store",
            headers: {
                "Authorization": `Bearer ${GetToken()}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: userName,
                balance: null
            }),
        });
        const data = await res.json();

        if (!res.ok) {
            setError(`${JSON.stringify(data.detail)}`)
        } else {
            localStorage.setItem('user', JSON.stringify(data));
            setUser(userName);
        }
    } catch (error) {
        setError("Error editing user: " + error);
    }
}

function GetToken() {
    return localStorage.getItem('access_token');
}

function GetUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

const AcceptInvitation = async (invitationId) => {
    try {
        const token = GetToken();
        await fetch(`${BACK_URL}/invitations/${invitationId}/accept`, {
            method: 'DELETE',
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            cache: "no-store",
        });
    } catch (err) {
        console.log(err);
    }
};

const RejectInvitation = async (invitation_id) => {
    
    try {
        const token = GetToken();
        await fetch(`${BACK_URL}/invitations/${invitation_id}/reject`, {
            method: 'DELETE',
            headers: {
                "Authorization": `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            cache: "no-store",
        });

    } catch (err) {
        console.log(err);
    }
};

const ApplySavedTheme = () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.documentElement.classList.add('light-mode');
    } else {
        document.documentElement.classList.remove('light-mode');
    }
};

const TypeChart = {
    GROUPS: 0,
    PAYMENTS_IN_GROUP: 1,
    PAYMENTS_IN_USER: 2,
    DEBTS_IN_GROUP: 3,
    DEBTS_IN_USER: 4
  };

const ViewType = {
    USER_CHARTS: 0,
    GROUP_CHARTS: 1,
}

function TrimField(s) {
  return s.trim()
}

export { BACK_URL, MAX_NAME_LENGTH, HandleSignIn, GetToken, GetUser, LogOut, EditUser, AcceptInvitation, RejectInvitation, ApplySavedTheme, TypeChart, ViewType, TrimField };