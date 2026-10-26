#include <math.h>

typedef struct {
    double kp;
    double kd;
} PDGains;

typedef struct {
    double torque;
    double position_error;
    double velocity_error;
} ActuatorStep;

ActuatorStep pd_impedance_step(double target_pos, double target_vel,
                               double current_pos, double current_vel,
                               PDGains gains) {
    ActuatorStep out;
    out.position_error = target_pos - current_pos;
    out.velocity_error = target_vel - current_vel;
    out.torque = (gains.kp * out.position_error) + (gains.kd * out.velocity_error);
    return out;
}

double foc_electrical_power(double phase_current, double phase_voltage) {
    return phase_current * phase_voltage;
}
