import {
  useUpdateClockDrift,
  useUpdateClockTime,
  useUpdateClockTimeSync,
} from "@/hooks/use-clock"
import { cn } from "@/lib/utils"
import { Label } from "@radix-ui/react-label"
import { useState } from "react"
import toast from "react-hot-toast"
import { Button } from "./ui/button"
import { Input } from "./ui/input"

interface Props {
  is_online: boolean
  time?: number
  is_leader?: boolean
  self_id?: number
  leader_id?: number
  drift?: number
  time_sync?: number
}

export function Clock(props: { clock: Props }) {
  const { mutate: updateClockDrift } = useUpdateClockDrift()
  const { mutate: updateClockTime } = useUpdateClockTime()
  const { mutate: updateClockTimeSync } = useUpdateClockTimeSync()
  const [drift, setDrift] = useState(props.clock.drift || 0)
  const [time, setTime] = useState(props.clock.time || 0)
  const [time_sync, setTimeSync] = useState(props.clock.time_sync || 0)

  function updateTime() {
    if (props.clock.self_id === undefined) return
    updateClockTime(
      {
        clockID: props.clock.self_id,
        time,
      },
      {
        onSuccess: () => {
          toast.success("Tempo alterado!")
        },
        onError: ({ message }) => {
          toast.error(message)
        },
      },
    )
  }

  function updateDrift() {
    if (props.clock.self_id === undefined) return
    updateClockDrift(
      {
        clockID: props.clock.self_id,
        drift,
      },
      {
        onSuccess: () => {
          toast.success("Drift alterado!")
        },
        onError: ({ message }) => {
          toast.error(message)
        },
      },
    )
  }

  function updateTimeSync() {
    if (props.clock.self_id === undefined) return
    updateClockTimeSync(
      {
        clockID: props.clock.self_id,
        time_sync,
      },
      {
        onSuccess: () => {
          toast.success("Tempo de sincronização alterado!")
        },
        onError: ({ message }) => {
          toast.error(message)
        },
      },
    )
  }

  return (
    <div>
      <h2
        className={cn("font-medium text-zinc-900", {
          "text-pink-700": props.clock.is_leader,
        })}
      >
        ID: {props.clock.self_id} -{" "}
        {props.clock.is_online ? "online" : "offline"}
      </h2>
      <div className="grid grid-cols-[160px_1fr] items-center">
        <ul className="space-y-1">
          <li>Tempo: {props.clock.time}</li>
          <li>Drift: {props.clock.drift}</li>
          <li>Leader ID: {props.clock.leader_id}</li>
          <li>Time Sync: {props.clock.time_sync}</li>
        </ul>
        <div className="space-y-2">
          <div className="grid grid-cols-3 items-center gap-1">
            <Label htmlFor="drift">Drift:</Label>
            <Input
              id="drift"
              type="number"
              value={drift}
              onChange={(e) => setDrift(Number(e.currentTarget.value))}
              min={0.1}
              step={0.1}
            />
            <Button onClick={updateDrift} variant="pink">
              Salvar
            </Button>
          </div>

          <div className="grid grid-cols-3 items-center gap-1">
            <Label htmlFor="time">Time:</Label>
            <Input
              id="time"
              type="number"
              value={time}
              onChange={(e) => setTime(Number(e.currentTarget.value))}
              min={1}
            />
            <Button onClick={updateTime} variant="pink">
              Salvar
            </Button>
          </div>
          <div className="grid grid-cols-3 items-center gap-1">
            <Label htmlFor="time_sync">Sync:</Label>
            <Input
              id="time_sync"
              type="number"
              value={time_sync}
              onChange={(e) => setTimeSync(Number(e.currentTarget.value))}
              min={3}
              max={10}
            />
            <Button onClick={updateTimeSync} variant="pink">
              Salvar
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
