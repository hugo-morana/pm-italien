-- Table de progression : une ligne par utilisateur et par clé (srs_noms, srs_verbes…, historique)
create table if not exists public.progress (
  user_id uuid not null default auth.uid() references auth.users on delete cascade,
  key text not null,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, key)
);

-- Chacun ne voit et ne modifie que ses propres lignes
alter table public.progress enable row level security;

create policy "lire sa progression" on public.progress
  for select to authenticated using (auth.uid() = user_id);
create policy "créer sa progression" on public.progress
  for insert to authenticated with check (auth.uid() = user_id);
create policy "modifier sa progression" on public.progress
  for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "supprimer sa progression" on public.progress
  for delete to authenticated using (auth.uid() = user_id);
