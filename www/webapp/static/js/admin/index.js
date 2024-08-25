async function fetchCourses() {
    const { user } = globalThis.user;
    const items = [];

    if (user.user_type === UserTypes.TEACHER) {
        items.push({
            'field': 'teacher_id', 
            'operator': 'equal',
            'value': user.id
        });
    }

    const params = new URLSearchParams({
        'page': 1,
        'per_page': 10
    });

    const res = await fetch('/api/course?'+params, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': sessionStorage.getItem('token')
        },
        body: JSON.stringify({
            'filters': {
                'items': items
            }
        })
    });
    
    if (!res.ok) {
        return [];
    }

    const courses = await res.json();

    return courses || [];
}

async function updateCourseTable() {
    const courses = await fetchCourses();
 
    if (courses.length === 0) {
        return;
    }

    document.getElementById('coursesPlaceholder').classList.add('d-none');
    
    document.getElementById('courses').innerText = courses;
}

