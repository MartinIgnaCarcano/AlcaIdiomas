const API_URL = 'http://localhost:5000/api';

async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "email": email, "contrasena": password })
        });

        if (!response.ok) {
            throw new Error('Credenciales incorrectas mi vieja es re puta');
        } else {
            const data = await response.json();
            localStorage.setItem('token', data.access_token); // Almacena el token en localStorage
            return true;
        }
    } catch (error) {
        console.error('Error al iniciar sesión:', error.message);
    }
}

document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const errorDiv = document.getElementById('loginError');

    try {
        console.log('email:', email);
        console.log('password:', password);

        const response = await login(email, password);
        if (response) {
            // 2️⃣ Ocultar (si estaba) el mensaje de error
            errorDiv.style.display = 'none';

            // 4️⃣ Cerrar el modal de Bootstrap
            const modalEl = document.getElementById('loginModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            // 5️⃣ Cambiar botón "Login" → "Mi Perfil"
            renderSessionMenu();

            // 8️⃣ (Opcional) Limpiar el formulario de login para la próxima vez
            document.getElementById('loginForm').reset();

        }
    } catch (err) {
        // Si el backend devolvió error o hubo problema de red
        console.error(err);
        alert('Credenciales incorrectas. Por favor, inténtalo de nuevo.');
        errorDiv.style.display = 'block';
    }
});

async function register(user) {
    try {
        const response = await fetch(`${API_URL}/usuarios`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (!response.ok) {
            throw new Error('Error en el registro');
        }

        return await response.json();
    } catch (error) {
        console.error('Error al registrar:', error.message);
        throw error;
    }
}

document.getElementById('registrationForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const contrasena = document.getElementById('regPassword').value;
    const contrasenaConfirm = document.getElementById('regPasswordConfirm').value;

    if (contrasena !== contrasenaConfirm) {
        alert('Las contraseñas no coinciden');
        return;
    }

    const user = {
        nombre: document.getElementById('firstName').value,
        apellido: document.getElementById('lastName').value,
        email: document.getElementById('regEmail').value,
        fecha_nacimiento: document.getElementById('birthdate').value,
        contrasena: document.getElementById('regPassword').value
    };

    const loading = document.getElementById('regLoading');
    const success = document.getElementById('regSuccess');
    const error = document.getElementById('regError');

    loading.style.display = 'block';
    success.style.display = 'none';
    error.style.display = 'none';

    try {
        await register(user);
        loading.style.display = 'none';
        success.style.display = 'block';
        document.getElementById('registrationForm').reset();
    } catch {
        loading.style.display = 'none';
        error.style.display = 'block';
    }
});

document.getElementById("logoutBtn").addEventListener("click", function (e) {
    e.preventDefault();
    console.log("Logout button clicked");
    localStorage.removeItem("token");
    renderSessionMenu();
});

