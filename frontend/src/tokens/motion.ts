export const motionTokens = {
  durations: {
    micro: 0.1,   // 100ms
    small: 0.15,  // 150ms
    medium: 0.2,  // 200ms
    large: 0.3,   // 300ms
  },
  easings: {
    standard: [0.4, 0.0, 0.2, 1],
    decelerate: [0.0, 0.0, 0.2, 1],
    accelerate: [0.4, 0.0, 1.0, 1],
  },
} as const;
