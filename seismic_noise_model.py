import numpy as np

def generate_ground_motion(duration=10.0, fs=1000):
    t = np.linspace(0, duration, int(duration * fs))
    microseismic = 2.5 * np.sin(2 * np.pi * 0.2 * t)
    cultural = 0.8 * np.sin(2 * np.pi * 4.5 * t)
    sensor_noise = np.random.normal(0, 0.15, len(t))
    return t, microseismic + cultural + sensor_noise

if __name__ == "__main__":
    t, motion = generate_ground_motion()
    rms = np.sqrt(np.mean(motion**2))
    print(f"Generated {len(t)} samples of multi-band terrestrial seismic motion.")
    print(f"Uncontrolled Ground RMS Displacement: {rms:.4f} um")
