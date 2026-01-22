# Cerebellum Engine

**Version**: v0.6.0-beta  
**Status**: Production Ready  
**License**: MIT License

---

## 📖 What is the Cerebellum?

The cerebellum is a brain structure located below the occipital lobe that **transforms memory into immediate action**.

### Biological Role

1. **Motor Control**: Precise movement regulation
2. **Predictive Control**: Anticipates and corrects future errors
3. **Learning**: Learns patterns from repetitive actions and improves performance
4. **Tremor Suppression**: Filters fine vibrations to maintain stable movement

### Relationship with Hippocampus

- **Hippocampus**: Decides "what to remember"
- **Cerebellum**: "Transforms memory into immediate action"

The cerebellum converts memories stored by the hippocampus into immediate control signals for precise actions.

---

## 🎯 Core Features of Cerebellum Engine

### 1. Predictive Feedforward

**Formula**: `e_pred(t+Δt) = e(t) + v(t)·Δt + ½a(t)·(Δt)²`

Predicts future errors in advance to correct them before they occur. Accounts for physical system delays to respond proactively.

**Application Examples**:
- Robot arm trajectory correction before reaching target
- Aircraft attitude control considering aerodynamic delays

### 2. Trial-to-Trial Correction

**Formula**: `trial_error = e(t) - b_hip(x(t), c(t))`

Remembers recurring errors in repetitive trajectories and eliminates them in subsequent trials. Same mechanism as humans learning instruments or sports.

**Application Examples**:
- Eliminating subtle deviations in repetitive CNC machining
- Improving accuracy in repetitive robot arm movements

### 3. Variance Reduction (Tremor Filtering)

**Formula**: `high_freq_noise = e(t) - filtered_error`

Removes high-frequency noise (tremor) while preserving low-frequency intentional movement. Implements cerebellar Tremor Suppression.

**Application Examples**:
- Removing fine tremors in surgical robots
- Vibration filtering in precision machining

### 4. Memory-Based Adaptation (Hippocampus Integration)

**Formula**: `memory_correction = -b_hip(x(t), c(t)) · α_memory · confidence · context_weight`

Converts hippocampal memory into immediate action. Applies different corrections based on context even at the same position.

**Application Examples**:
- Automatic correction of temperature-dependent errors
- Adaptive control based on tools or environment

---

## 🏭 Industrial Applications

### 1. Precision Machining (Priority 1)
- **5-axis CNC machines**: Ultra-precision machining at 0.00001mm scale
- **Micro-machining**: Semiconductor manufacturing, medical devices
- **Diamond cutting**: Extreme precision operations

### 2. Robot Arm Control (Priority 2)
- **Industrial robot arms**: Pick and place, welding, assembly
- **Surgical robots**: Tremor removal, precise trajectory tracking
- **Service robots**: Smooth motion, stable control

### 3. Aircraft Control (Priority 3)
- **Autopilot systems**: Aerodynamic delay compensation
- **Drone control**: Stable hovering, precise trajectory tracking
- **Aircraft attitude control**: Smooth maneuvers

### 4. Other Fields
- Autonomous vehicles: Precise steering control
- Medical devices: Precise position control
- Semiconductor manufacturing: Extreme precision operations

---

## 🚀 Quick Start

### Installation

```bash
pip install numpy
```

### Basic Usage

```python
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig
import numpy as np

# Create cerebellum engine
config = CerebellumConfig(
    feedforward_gain=0.5,
    trial_gain=0.3,
    variance_gain=0.2,
    memory_gain=0.4
)
engine = CerebellumEngine(memory_dim=5, config=config)

# Compute correction
correction = engine.compute_correction(
    current_state=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    target_state=np.array([1.0, 1.0, 0.0, 0.0, 0.0]),
    velocity=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    acceleration=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    dt=0.001
)
```

### Integration with PID Controller

```python
# PID control (base control)
pid_output = pid_controller.compute(error)

# Cerebellum correction (precision correction)
cerebellum_correction = cerebellum.compute_correction(
    current_state=current_state,
    target_state=target_state,
    velocity=velocity,
    acceleration=acceleration,
    context={'mode': 'precision_control'},
    dt=0.001
)

# Final control signal (PID + Cerebellum)
final_control = pid_output + cerebellum_correction
```

---

## 📚 Documentation

- `FORMULA_REFERENCE.md`: Formula reference guide
- `INDUSTRIAL_APPLICATIONS.md`: Detailed industrial applications
- `MODULE_INTEGRATION_GUIDE.md`: Integration guide
- `EXPERT_REVIEW.md`: Expert review
- `WORK_LOG.md`: Work log

---

## 🧪 Testing

```bash
cd package
python3 run_all_tests.py
```

---

## 📝 Examples

```bash
# Precision machining example
python3 examples/precision_machining_example.py

# Robot arm control example
python3 examples/robot_arm_example.py

# Aircraft control example
python3 examples/aircraft_control_example.py

# Hovering learning
python3 scenarios/hovering_learning.py
```

---

## 📦 Modularity Principles

- ✅ **Independent Module**: Usable before full engine (Cookie Brain) completion
- ✅ **Plug and Play**: Easy integration with existing control systems
- ✅ **Minimal Dependencies**: Only NumPy required
- ✅ **Production Ready**: Directly applicable to real machines

---

## 🔬 Version Information

### v0.6.0-beta (Current Version)

**New Features**:
- Confidence-based gain adjustment: Adaptive correction based on memory confidence
- Error norm-based saturation: Prevents excessive correction signals
- Context weighting: Adaptive response based on situation

**Core Features**:
- Predictive Feedforward
- Trial-to-Trial Correction
- Variance Reduction
- Memory-Based Adaptation

---

## 👤 Author

GNJz

---

## 📄 License

MIT License

---

**Version**: v0.6.0-beta  
**Updated**: 2026-01-22

