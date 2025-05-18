"use client";

import { motion } from "motion/react";

interface SlideInProps {
  children?: React.ReactNode;
  direction?: keyof typeof transformMap;
  className?: string;
}

const directions = ["up", "right", "down", "left"] as const;
const directionToIndex = {
  up: 0,
  right: 1,
  down: 2,
  left: 3,
} as const;

const transformMap = {
  up: { y: 16 },
  right: { x: -16 },
  down: { y: -16 },
  left: { x: 16 },
};

export const SlideIn = (props: SlideInProps) => {
  const { children, direction = "up", className } = props;

  const oppositeDirection = directions[(directionToIndex[direction] + 2) % 4];

  return (
    <motion.div
      initial={{ opacity: 0, ...transformMap[direction] }}
      whileInView={{ opacity: 1, x: 0, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, ease: "easeInOut" }}
      exit={{ opacity: 0, ...transformMap[oppositeDirection] }}
      className={className}
    >
      {children}
    </motion.div>
  );
};
