-- Run this in the Supabase SQL editor to set up the tasks table.
-- If upgrading from a previous version, see the migration section below.

-- ============================================================
-- Fresh installation
-- ============================================================
create table if not exists public.tasks (
  id          bigint generated always as identity primary key,
  title       text        not null check (char_length(title) between 1 and 120),
  description text        not null default '' check (char_length(description) <= 500),
  status      text        not null default 'todo'   check (status in ('todo', 'in_progress', 'done')),
  priority    text        not null default 'medium' check (priority in ('low', 'medium', 'high')),
  created_at  timestamptz not null default timezone('utc', now()),
  updated_at  timestamptz not null default timezone('utc', now())
);

-- Auto-update updated_at on every row change
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = timezone('utc', now());
  return new;
end;
$$;

drop trigger if exists trg_tasks_updated_at on public.tasks;
create trigger trg_tasks_updated_at
before update on public.tasks
for each row execute function public.set_updated_at();

-- ============================================================
-- Migration (run only if upgrading from the previous schema)
-- ============================================================
-- alter table public.tasks
--   add column if not exists priority text not null default 'medium'
--     check (priority in ('low', 'medium', 'high'));
