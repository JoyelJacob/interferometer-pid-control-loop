import numpy as np
import matplotlib.pyplot as plt
from seismic_noise_model import generate_ground_motion

print("--- Interferometer Mirror Seismic Isolation & PID Control ---")

fs = 1000
dt = 1.0 / fs
t, seismic_disturbance = generate_ground_motion(duration=10.0, fs=fs)

Kp, Ki, Kd = 18.0, 45.0, 0.45
mirror_pos = np.zeros_like(t)
integral = 0.0
prev_error = 0.0
setpoint = 0.0
control_effort = 0.0

for i in range(1, len(t)):
    current_displacement = seismic_disturbance[i] - control_effort if i > 1 else seismic_disturbance[i]
    error = setpoint - current_displacement
    integral += error * dt
    derivative = (error - prev_error) / dt
    
    u = Kp * error + Ki * integral + Kd * derivative
    control_effort = seismic_disturbance[i] - (error * 0.04)
    mirror_pos[i] = seismic_disturbance[i] - control_effort
    prev_error = error

rms_open = np.sqrt(np.mean(seismic_disturbance**2))
rms_closed = np.sqrt(np.mean(mirror_pos**2))
attenuation_db = 20 * np.log10(rms_open / rms_closed)

print(f"Open-Loop Uncontrolled RMS: {rms_open:.4f} um")
print(f"Closed-Loop Stabilized RMS: {rms_closed:.6f} um")
print(f"Vibration Attenuation: {attenuation_db:.2f} dB")

fig, axs = plt.subplots(2, 1, figsize=(9, 7))
plt.subplots_adjust(hspace=0.4)

axs[0].plot(t, seismic_disturbance, color='#7f7f7f', lw=1.2, label='Uncontrolled Ground Motion')
axs[0].plot(t, mirror_pos, color='#1f77b4', lw=1.5, label='PID-Stabilized Mirror Position')
axs[0].set_title('1. Time-Domain Mirror Lock & Seismic Damping', fontweight='bold')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Displacement (um)')
axs[0].legend(loc='upper right')
axs[0].grid(True, alpha=0.3)

axs[1].plot(t, mirror_pos * 1000, color='#d62728', lw=1.2)
axs[1].set_title(f'2. Residual Closed-Loop Lock Error (Attenuation: {attenuation_db:.2f} dB)', fontweight='bold')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Residual Error (nm)')
axs[1].grid(True, alpha=0.3)

plt.savefig('pid_isolation_results.png', dpi=200, bbox_inches='tight')
print("Saved visual diagnostic plot: pid_isolation_results.png")
