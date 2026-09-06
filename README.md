# StrideSense

StrideSense is a foot-mounted wearable prototype for collecting and analyzing running motion data using a Raspberry Pi Pico WH and an MPU-6050 inertial measurement unit.

I started the project because I run regularly and was interested in whether inexpensive wearable hardware could be used to learn more about running mechanics. The long-term goal is to turn raw acceleration and gyroscope measurements into useful metrics such as cadence, stride timing, and gait consistency.

This is still an active project, so the repository includes both working components and smaller test programs used while bringing the hardware and analysis pipeline together.

## Current Status

The project is currently in the hardware validation and data collection stage.

So far, I have:

- Set up and tested the Raspberry Pi Pico WH
- Selected and connected the MPU-6050 accelerometer and gyroscope
- Written basic hardware and IMU test programs
- Built a Python pipeline for reading and visualizing motion data
- Created the structure for moving data from the sensor into later gait analysis

Current work is focused on reliably collecting real IMU measurements during movement.

After that, the next step is to process the signals and identify individual stride events.

## Hardware

- Raspberry Pi Pico WH
- Adafruit MPU-6050 6-DoF Accelerometer and Gyroscope
- STEMMA QT / Qwiic connection
- Portable power source
- Foot-mounted enclosure / strap

## How It Works

The basic pipeline is:

```text
MPU-6050
    ↓
Raspberry Pi Pico WH
    ↓
Acceleration + Gyroscope Measurements
    ↓
Motion Data
    ↓
Python Analysis
    ↓
Stride and Gait Metrics
```

The MPU-6050 provides acceleration along three axes and angular velocity along three axes.

The Pico reads those measurements over I2C and can output them for storage and later analysis.

The analysis side of the project is being built in Python so I can experiment with filtering, visualization, stride detection, and eventually higher-level gait metrics.

## Repository Structure

```text
StrideSense/
├── firmware/
│   ├── blink_test.py
│   └── imu_test.py
├── analysis/
│   └── plot_motion.py
├── data/
│   └── sample_synthetic_data.csv
├── docs/
│   └── hardware_setup.md
└── README.md
```

### `firmware/`

MicroPython programs that run on the Raspberry Pi Pico WH.

`blink_test.py` was used as an initial hardware validation step.

`imu_test.py` communicates with the MPU-6050 over I2C and prints accelerometer and gyroscope measurements.

### `analysis/`

Python scripts for inspecting and visualizing collected motion data.

### `data/`

Test datasets used while developing the analysis pipeline.

Any synthetic data is labeled as synthetic and is only used to test the software before enough real sensor data is collected.

### `docs/`

Notes about hardware configuration, wiring, and the overall project architecture.

## Roadmap

### Phase 1 — Hardware setup
- [x] Configure Raspberry Pi Pico WH
- [x] Validate Pico with basic test firmware
- [x] Connect MPU-6050
- [x] Build initial IMU communication test

### Phase 2 — Data collection
- [ ] Collect continuous accelerometer and gyroscope data
- [ ] Store timestamped sensor readings
- [ ] Test the device during walking and running
- [ ] Build repeatable recording sessions

### Phase 3 — Signal processing
- [ ] Filter noisy sensor measurements
- [ ] Detect repeated stride events
- [ ] Estimate cadence
- [ ] Measure stride timing consistency

### Phase 4 — Visualization
- [ ] Visualize gait sessions
- [ ] Compare runs over time
- [ ] Explore additional gait metrics

## Why I Built It

StrideSense is partly a running project and partly a way for me to learn by building something that crosses several areas of computer science.

Instead of making another purely software-based project, I wanted to work with physical sensors and understand the entire path from hardware input to usable data.

The project has pushed me to work with:

- Microcontrollers
- I2C communication
- Sensor data
- Python
- Hardware debugging
- Data visualization
- Signal processing concepts

There is still a lot left to build, but that is also the point of the project. I am using each stage to get more comfortable working with hardware and writing the software myself instead of treating the final product as a black box.

## Development

StrideSense is an in-progress personal project.

Some of the code in this repository consists of small testing utilities because I am building and validating each layer separately before combining them into a larger system.

The immediate goal is to get reliable real-world motion data from the MPU-6050. From there, I will continue developing the analysis pipeline and gait metrics.
