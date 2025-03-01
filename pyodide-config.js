// 配置加载进度提示
let loadingMessage = document.createElement('div');
loadingMessage.innerHTML = '加载运行时环境 (约需15秒)...';
document.body.prepend(loadingMessage);

// 错误处理
window.addEventListener('pyodideError', e => {
    console.error('Pyodide Error:', e.detail);
    loadingMessage.innerHTML = `错误: ${e.detail.message}`;
});