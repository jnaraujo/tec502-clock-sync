import { env } from "@/env"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

export interface ClockData {
  is_online: boolean
  time?: number
  is_leader?: boolean
  self_id?: number
  leader_id?: number
  drift?: number
}

export function useClocksData() {
  return useQuery({
    queryFn: async ({ signal }) => {
      const responses = await Promise.allSettled(
        env.VITE_BANKS.map((url) =>
          fetch(`${url}/clock`, {
            signal,
          }),
        ),
      )

      const clocks: Array<ClockData> = []
      for (const resp of responses) {
        if (resp.status === "fulfilled") {
          const data = await resp.value.json()
          clocks.push({
            is_online: true,
            ...data,
          })
        } else {
          clocks.push({
            is_online: false,
          })
        }
      }
      return clocks
    },
    refetchInterval: 1_000,
    queryKey: ["clockData"],
  })
}

export function useUpdateClockTime() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: { clockID: number; time: number }) => {
      const resp = await fetch(
        `${env.VITE_BANKS.at(data.clockID)}/internal/time/${data.time}`,
        {
          method: "POST",
        },
      )
      if (!resp.ok) {
        throw new Error("Erro ao alterar o tempo do relógio.")
      }
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["clockData"],
      })
    },
  })
}

export function useUpdateClockDrift() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: { clockID: number; drift: number }) => {
      const resp = await fetch(
        `${env.VITE_BANKS.at(data.clockID)}/drift/${data.drift}`,
        {
          method: "POST",
        },
      )
      if (!resp.ok) {
        throw new Error("Erro ao alterar o drift do relógio.")
      }
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["clockData"],
      })
    },
  })
}
