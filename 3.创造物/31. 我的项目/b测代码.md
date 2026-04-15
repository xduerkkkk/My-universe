
```

% b测：QPSK已调信号生成仿真

clear; clc; close all;

%% 总体参数与过程参数

fc = 20; % 载波频率，取值范围5-100的5的倍数

Rb = 20; % 源码比特速率，数值上=载波频率

fs = 20 * fc; % 采样率 ，为了让波形平滑，取载波频率的20倍

Ts = 1 / fs; % 采样时间间隔

Tb = 1 / Rb; % 每个比特的持续时间

T_sym = 2 * Tb; % QPSK符号周期，1个符号含2个比特

%%生成周期为63bits的m序列

% 使用6级线性移位寄存器产生，本原多项式设为 f(x) = x^6 + x + 1

reg = [1 0 0 0 0 0];

m_seq = zeros(1, 63);

for i = 1:63

m_seq(i) = reg(6);

new_bit = xor(reg(6), reg(1)); %模2加法反馈

reg = [new_bit, reg(1:5)]; %移位

end

% QPSK每次需映射2个比特。但63是奇数，无法整除。

% 解决办法：我们将m序列连续产生2个周期，得到126个比特，正好可以映射为63个QPSK符号。

data_bits = [m_seq, m_seq];

N_bits = length(data_bits);

%%串并转换与双极性映射 (0->-1, 1->1)

I_bits = data_bits(1:2:end); % 奇数位分给 I 路

Q_bits = data_bits(2:2:end); % 偶数位分给 Q 路

I_level = 2 * I_bits - 1; % 映射为双极性 -1 和 +1

Q_level = 2 * Q_bits - 1;

%% 生成基带波形 (用于绘图和调制)

% 将离散的符号扩展为时间上的连续波形

samples_per_sym = T_sym / Ts;

I_wave = kron(I_level, ones(1, samples_per_sym));

Q_wave = kron(Q_level, ones(1, samples_per_sym));

% 源码信号波形

data_level = 2 * data_bits - 1;

samples_per_bit = Tb / Ts;

source_wave = kron(data_level, ones(1, samples_per_bit));

t_source = (0:length(source_wave)-1) * Ts; % 时间轴

%% QPSK 调制

t = (0:length(I_wave)-1) * Ts; % 符号时间轴

carrier_I = cos(2 * pi * fc * t); % 同相载波

carrier_Q = -sin(2 * pi * fc * t); % 正交载波

% 调制信号 = I路 * 同相载波 + Q路 * 正交载波

qpsk_signal = I_wave .* carrier_I + Q_wave .* carrier_Q;

figure('Name', 'QPSK仿真结果', 'Position', [100, 100, 1000, 800]);

% 1. 观测源码时域波形 (项目2)

subplot(2,2,1);

plot(t_source, source_wave, 'LineWidth', 1.5);

axis([0 20*Tb -1.5 1.5]); % 只截取前20个比特展示，以免太密看不清

title('源码信号时域波形 (截取前20 bits)');

xlabel('时间 (ms)'); ylabel('幅度'); grid on;

% 2. 观测基带信号发射端星座图 (项目3)

subplot(2,2,2);

scatter(I_level, Q_level, 100, 'filled', 'MarkerFaceColor', 'r');

axis([-2 2 -2 2]); grid on;

title('基带信号发射端星座图');

xlabel('同相分量 (I)'); ylabel('正交分量 (Q)');

xline(0, 'k--'); yline(0, 'k--');

% 3. 观测已调信号时域波形 (项目2)

subplot(2,2,3);

plot(t, qpsk_signal, 'LineWidth', 1.2);

axis([0 10*T_sym -2 2]); % 截取前10个符号展示

title('QPSK已调信号时域波形 (截取前10个符号)');

xlabel('时间 (ms)'); ylabel('幅度'); grid on;

% 4. 观测已调信号的频谱 (项目4)

N_fft = 2048; % FFT点数

f = (-N_fft/2:N_fft/2-1) * (fs / N_fft); % 频率轴 (kHz)

QPSK_spectrum = fftshift(fft(qpsk_signal, N_fft)); % 傅里叶变换并移到中心

Pxx = 10*log10(abs(QPSK_spectrum).^2 / N_fft); % 计算功率谱密度(dB)

subplot(2,2,4);

plot(f, Pxx, 'LineWidth', 1.5);

xlim([-fc*3 fc*3]); % 限制显示的频率范围

title('QPSK已调信号功率谱');

xlabel('频率 (kHz)'); ylabel('功率谱密度 (dB)'); grid on;
```

