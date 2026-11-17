-- Palais : table de progression + suppression de son compte
create table if not exists public.progress (
  user_id uuid not null default auth.uid() references auth.users on delete cascade,
  key text not null,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, key)
);
alter table public.progress enable row level security;
drop policy if exists "lire sa progression" on public.progress;
drop policy if exists "créer sa progression" on public.progress;
drop policy if exists "modifier sa progression" on public.progress;
drop policy if exists "supprimer sa progression" on public.progress;
create policy "lire sa progression" on public.progress for select to authenticated using (auth.uid() = user_id);
create policy "créer sa progression" on public.progress for insert to authenticated with check (auth.uid() = user_id);
create policy "modifier sa progression" on public.progress for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "supprimer sa progression" on public.progress for delete to authenticated using (auth.uid() = user_id);

-- Supprimer son propre compte (et seulement le sien)
create or replace function public.delete_my_account() returns void
language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'non connecté'; end if;
  delete from public.progress where user_id = auth.uid();
  delete from auth.users where id = auth.uid();
end $$;
revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;
