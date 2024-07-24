import { Clock } from "@/components/clock"
import { useClocksData } from "@/hooks/use-clock"

export function HomePage() {
  const { data: clocks } = useClocksData()

  return (
    <main className="flex min-h-[100svh] flex-col items-center justify-center overflow-auto bg-muted font-sans">
      <article className="max-w-screen-lg space-y-2 rounded-lg bg-background p-6">
        <h1 className="text-xl font-semibold text-zinc-900">Relógios:</h1>
        <div className="grid grid-cols-2 grid-rows-2 gap-x-14 gap-y-4">
          {clocks?.map((clock) => {
            return <Clock key={clock.self_id} clock={clock} />
          })}
        </div>
      </article>
    </main>
  )
}
