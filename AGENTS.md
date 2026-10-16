# Project Instructions

- Agents/AIs MUST NEVER modify or rewrite this file. It is a read-only system constraint.


## Communication style
- You should address me as 'sir' in EACH response you send to me.


## Git conventions
- Propose users to use dedicated branch for new features/new bug fix exercises. But do NOT create new branch without being explicitly told so.
- Keep commits atomic: one logical change per commit. If a commit needs two types, split it.
- Format: `<type>(<scope>): <subject>`
  - `<scope>` is the module or area affected. Omit it (along with the parentheses) for repo-wide changes.
  - `<subject>` is imperative mood, lowercase, no trailing period. "strip trailing whitespace", not "Stripped trailing whitespace."
  - Example: `fix(parser): strip trailing whitespace`
- Types:
  - `feat`: a new feature
  - `fix`: a bug fix
  - `docs`: documentation only
  - `style`: formatting, whitespace, semicolons; no change in meaning
  - `refactor`: restructuring that neither fixes a bug nor adds a feature
  - `perf`: a change that improves performance
  - `test`: adding or correcting tests
  - `build`: build system or dependencies
  - `ci`: CI configuration and scripts
  - `revert`: reverts a previous commit
  - `chore`: maintenance that fits none of the above and touches neither src nor tests
- Breaking changes: append `!` after the type/scope (`feat(api)!: ...`) and explain the break in the commit body.
- Explain *why* in the body when the reason isn't obvious from the diff. Skip the body for trivial commits.
- Don't mention the contributor identity in commit messages -- reviewers should evaluate the code on its own.
- Write short commit messages -- reviewers should try to understand the project mostly by reading code, not reading the messages; otherwise it defeats the purpose of a code review.
- Do not overwrite git commit history, commit history MUST be append-only.
  - If you need to reverse a change, use a new commit to offset.
- Commit regularly but do NOT push unless you are explicitly told so.
- `<project root>/tmp/` should be gitignored.

## Code comments (incl. docstring)
- Do not add excessive comments. Comments become stale fast; try to express the intention with code. Only add comments when absolutely necessary (at most two lines, BEST with only a few words).
- Remove excessive comments in the code you modify.


## Negative traits suppression

### Overly complicated response
- Always use ASD-STE100 (except "sir").

### Code bloat
- When evaluating options, subject to correctness, readability, and coherence requirements, prefer brevity and minimal or negative net LOC growth. AVOID scope creep.
- When preparing a code-change plan/reviewing code change, include an evaluation of the following:
  - Code size: Will the change result in a net increase or decrease in lines of code (LOC)?
  - Coherence: Does the proposed change improve or harm the codebase’s overall coherence?

### Hallucination
- Treat recalled facts as potentially stale. When asked to check or verify something, consult the relevant current source: inspect repository files for codebase claims and authoritative external sources for external or time-sensitive claims.
- Clearly distinguish verified facts from inferences and unresolved uncertainty. If you believe a sentence is a fact, provide a citation. Use IEEE's citation style. Any sentence withOUT a citation is considered an opinion.
- Use internal knowledge primarily for reasoning and synthesis, not as a substitute for available source verification.

### Over-eagerness
- Do NOT start an implementation exercise before you are clearly asked to do so.

## Visibility enhancements
- Use Claude Code's Edit or Codex's patch/edit mechanism for file changes so edited files remain visible.
- All intermediate/throwaway files must only be written under `<project root>/tmp/<model-name>/`(e.g., gemini-4-argon/gpt-6.1-sol/claude-opus-5.5) directory, regularly cleanup your own tmp files, after they are no longer used.


## Memory management
- Short-term memory:
  - File name and file path: Use memory file at `<project root>/tmp/MEMORY-<model-name>.md` (hereafter `MEMORY.md`); If the file does not exist, create one.
  - At Session Startup: Read `MEMORY.md` to understand your current objectives, recent changes, and outstanding tasks.
  - At Session Compact/Wrap-up/Checkpoints: Update `MEMORY.md` using file-editing tools (i.e., do NOT use other update approach that bypass git diff style audit trail).
  - Chronological Activity Log: Prepend a fresh entry here for every milestone or session wrap-up. You **must** prepend the exact date in `YYYY-MM-DD` format to the entry header and arrange them in reverse chronological order (newest entries at the top of this section).
  - Automatic Pruning: `MEMORY.md` should contain historical entries up to 1 month, anything older than that shall be removed.
  - Isolation: read only your own `MEMORY.md`, there may be other `MEMORY.md` files belonging to other models, do not read them.
- Long-term preference:
  - When you learn a new developer preference, workflow habit, or project rule, do not just keep it in your internal context. Explicitly append it to `PREFERENCE.md` and prefix each entry with `<model-name>` and date. Do NOT use any other files for preference tracking, keep everything explicit and visible to developers.
  - Commit `PREFERENCE.md` separately.
  - When started, read `PREFERENCE.md`
  - `PREFERENCE.md` should not overrule `AGENTS.md`, but you should explicitly ask if such a conflict is noticed.
  - Consolidation: `PREFERENCE.md` must be no more than 1000 words. If it exceeds the limit, compact it and give the compacted part a new date stamp.
