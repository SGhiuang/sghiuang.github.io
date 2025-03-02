const auth0 = await createAuth0Client({
    domain: 'dev-x2xv40s2d6q5f4qs.us.auth0.com',
    client_id: 'QcBaTowTveySgflw0B3i2i4aHcbGlcj3',
    redirect_uri: window.location.origin + '/callback.html',
    audience: 'https://dev-x2xv40s2d6q5f4qs.us.auth0.com/api/v2/', // 按需配置
    scope: 'openid profile email'
  });
  
  // 登录处理
  document.getElementById('login').addEventListener('click', async () => {
    await auth0.loginWithRedirect();
  });
  
  // 检查认证状态
  const isAuthenticated = await auth0.isAuthenticated();
  if (isAuthenticated) {
    window.location.href = '/dashboard.html';
  }