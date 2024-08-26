UserTypes = Object.freeze({
    TEACHER: 'TEACHER',
    STUDENT: 'STUDENT',
    ADMIN: 'ADMIN'
});

function authorizer(userTypes) {
    const { user } = globalThis.user;
    
    if (!userTypes.includes(user.user_type)) {
        window.location.href = '/';
    }
}

