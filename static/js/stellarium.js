let stel; // Stellarium Web 实例

// 初始化 Stellarium
function initStellarium() {
    stel = new Stellarium.Stellarium({
        container: document.getElementById('stellarium-container'),
        config: {
            latitude: parseFloat(document.getElementById('latitude').value),
            longitude: parseFloat(document.getElementById('longitude').value),
            altitude: parseFloat(document.getElementById('altitude').value),
            date: new Date().toISOString(), // 初始时间为当前 UTC 时间
            showGrid: true,
            showConstellationLabels: true,
            // 其他默认配置
            fov: 60, // 视野角度
            antialias: true, // 抗锯齿
            atmosphere: true, // 显示大气层
        }
    });

    // 初始化时间选择器（转换为本地时间显示）
    const timePicker = document.getElementById('time-picker');
    const currentDate = new Date();
    timePicker.value = currentDate.toISOString().split('T')[0] + 'T' + currentDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// 应用配置函数
function applyConfiguration() {
    const config = {
        latitude: parseFloat(document.getElementById('latitude').value),
        longitude: parseFloat(document.getElementById('longitude').value),
        altitude: parseFloat(document.getElementById('altitude').value),
        date: new Date(document.getElementById('time-picker').value).toISOString(),
        showGrid: document.getElementById('show-grid').checked,
        showConstellationLabels: document.getElementById('show-constellations').checked,
    };

    stel.setConfig(config); // 更新配置
}

// 控制面板交互
document.getElementById('toggle-controls').addEventListener('click', () => {
    document.getElementById('control-panel').classList.toggle('active');
});

document.getElementById('close-panel').addEventListener('click', () => {
    document.getElementById('control-panel').classList.remove('active');
});

document.getElementById('apply-changes').addEventListener('click', applyConfiguration);

// 页面加载后初始化
window.addEventListener('load', initStellarium);