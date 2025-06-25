import { useState, useEffect, useCallback } from 'react';

interface UseApiResponse<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export function useApi<T>(
  fetchFunction: () => Promise<T>,
  deps: any[] = []
): UseApiResponse<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await fetchFunction();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('An error occurred'));
    } finally {
      setLoading(false);
    }
  }, [fetchFunction]);

  useEffect(() => {
    fetchData();
  }, [...deps, fetchData]);

  return { data, loading, error, refetch: fetchData };
}

export function useApiMutation<T, U = any>(
  mutationFunction: (data: U) => Promise<T>
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const mutate = async (mutationData: U) => {
    try {
      setLoading(true);
      setError(null);
      const result = await mutationFunction(mutationData);
      setData(result);
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('An error occurred');
      setError(error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, mutate };
}

export function useInfiniteApi<T>(
  fetchFunction: (page: number) => Promise<T[]>,
  pageSize: number = 10
) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);

  const loadMore = useCallback(async () => {
    if (loading || !hasMore) return;

    try {
      setLoading(true);
      setError(null);
      const newData = await fetchFunction(page);
      if (newData.length < pageSize) {
        setHasMore(false);
      }
      setData(curr => [...curr, ...newData]);
      setPage(p => p + 1);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('An error occurred'));
    } finally {
      setLoading(false);
    }
  }, [fetchFunction, loading, hasMore, page, pageSize]);

  useEffect(() => {
    loadMore();
  }, []); // Load first page on mount

  return { data, loading, error, hasMore, loadMore };
}
