import { z } from "zod"

const envSchema = z.object({
  VITE_BANKS: z.string().transform((val) => val.split(",")),
})

export const env = envSchema.parse(import.meta.env)
