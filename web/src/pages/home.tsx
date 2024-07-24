import { Clock } from "@/components/clock"
import { useClocksData } from "@/hooks/use-clock"

export function HomePage() {
  const { data: clocks } = useClocksData()

  return (
    <main className="flex min-h-[100svh] flex-col items-center justify-center overflow-auto bg-muted font-sans">
      <article className="w-[450px] space-y-2 rounded-lg bg-background p-6">
        <h1 className="text-xl font-semibold text-zinc-900">Relógios:</h1>
        <div className="space-y-2">
          {clocks?.map((clock) => {
            return <Clock key={clock.self_id} clock={clock} />
          })}
        </div>
      </article>
    </main>
  )
}
