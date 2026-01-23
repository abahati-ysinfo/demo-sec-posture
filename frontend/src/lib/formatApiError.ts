/**
 * Formats API error responses into user-friendly strings.
 * Handles FastAPI/Pydantic validation errors and other error formats.
 */
export function formatApiError(error: unknown, fallbackMessage = 'An error occurred'): string {
  if (!error) return fallbackMessage;

  const detail = (
    error as { response?: { data?: { detail?: string | unknown[] | { msg?: string } } } }
  ).response?.data?.detail;

  if (!detail) return fallbackMessage;

  if (typeof detail === 'string') return detail;

  if (Array.isArray(detail)) {
    const messages = detail
      .map((err: unknown) => {
        if (typeof err === 'string') return err;
        if (typeof err === 'object' && err !== null && 'msg' in err)
          return (err as { msg: string }).msg;
        return JSON.stringify(err);
      })
      .filter(Boolean);

    return messages.length > 0 ? messages.join(', ') : fallbackMessage;
  }

  if (typeof detail === 'object' && detail !== null && 'msg' in detail) {
    return (detail as { msg: string }).msg;
  }

  if (typeof detail === 'object') {
    try {
      return JSON.stringify(detail);
    } catch {
      return fallbackMessage;
    }
  }

  return fallbackMessage;
}
