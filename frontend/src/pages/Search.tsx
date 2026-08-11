import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { searchService } from '../services';
import { Search as SearchIcon, Filter, Clock, Star, X } from 'lucide-react';

export function Search() {
  const [query, setQuery] = useState('');
  const [selectedEntityTypes, setSelectedEntityTypes] = useState<string[]>([]);
  const [debouncedQuery, setDebouncedQuery] = useState('');

  // Debounce search
  useState(() => {
    const timer = setTimeout(() => setDebouncedQuery(query), 300);
    return () => clearTimeout(timer);
  });

  const { data, isLoading } = useQuery({
    queryKey: ['search', debouncedQuery, selectedEntityTypes],
    queryFn: () => searchService.globalSearch(debouncedQuery, { 
      entity_types: selectedEntityTypes.length > 0 ? selectedEntityTypes : undefined 
    }),
    enabled: debouncedQuery.length > 2,
  });

  const { data: recentSearches } = useQuery({
    queryKey: ['recent-searches'],
    queryFn: searchService.getRecentSearches,
    enabled: debouncedQuery.length === 0,
  });

  const { data: savedSearches } = useQuery({
    queryKey: ['saved-searches'],
    queryFn: searchService.getSavedSearches,
  });

  const entityTypes = [
    { id: 'lead', name: 'Leads', icon: '👤' },
    { id: 'contact', name: 'Contacts', icon: '👥' },
    { id: 'company', name: 'Companies', icon: '🏢' },
    { id: 'deal', name: 'Deals', icon: '💰' },
    { id: 'activity', name: 'Activities', icon: '📅' },
  ];

  const toggleEntityType = (type: string) => {
    setSelectedEntityTypes(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const getEntityIcon = (type: string) => {
    const entity = entityTypes.find(e => e.id === type);
    return entity?.icon || '📄';
  };

  return (
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Search</h1>
          <div className="relative">
            <SearchIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search across leads, contacts, companies, deals, activities..."
              className="w-full pl-12 pr-4 py-4 border rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {query && (
              <button
                onClick={() => setQuery('')}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>

        <div className="mb-4 flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-500" />
          <div className="flex flex-wrap gap-2">
            {entityTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => toggleEntityType(type.id)}
                className={`px-3 py-1 rounded-full text-sm flex items-center gap-2 ${
                  selectedEntityTypes.includes(type.id)
                    ? 'bg-blue-100 text-blue-800'
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                }`}
              >
                <span>{type.icon}</span>
                {type.name}
              </button>
            ))}
          </div>
        </div>

        {query.length > 2 ? (
          <div>
            {isLoading ? (
              <div className="text-center py-8 text-gray-500">Searching...</div>
            ) : data?.results?.length > 0 ? (
              <div className="space-y-4">
                {data.results.map((result: any) => (
                  <div
                    key={`${result.type}-${result.id}`}
                    className="bg-white rounded-lg shadow p-4 hover:shadow-lg transition-shadow cursor-pointer"
                  >
                    <div className="flex items-start gap-4">
                      <span className="text-2xl">{getEntityIcon(result.type)}</span>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900">{result.title}</h3>
                          <span className="text-xs bg-gray-100 px-2 py-1 rounded capitalize">
                            {result.type}
                          </span>
                        </div>
                        {result.description && (
                          <p className="text-gray-600 mt-1">{result.description}</p>
                        )}
                        <div className="text-sm text-gray-500 mt-2">
                          Score: {Math.round(result.score * 100)}%
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                No results found for "{query}"
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-6">
            {recentSearches?.searches?.length > 0 && (
              <div>
                <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Clock className="w-5 h-5" />
                  Recent Searches
                </h2>
                <div className="flex flex-wrap gap-2">
                  {recentSearches.searches.map((search: any, index: number) => (
                    <button
                      key={index}
                      onClick={() => setQuery(search.query)}
                      className="bg-gray-100 px-3 py-1 rounded-full text-sm hover:bg-gray-200"
                    >
                      {search.query}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {savedSearches?.searches?.length > 0 && (
              <div>
                <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Star className="w-5 h-5" />
                  Saved Searches
                </h2>
                <div className="space-y-2">
                  {savedSearches.searches.map((search: any) => (
                    <button
                      key={search.id}
                      onClick={() => setQuery(search.query)}
                      className="w-full text-left bg-gray-50 px-4 py-2 rounded-lg hover:bg-gray-100"
                    >
                      <div className="font-medium">{search.name}</div>
                      <div className="text-sm text-gray-500">{search.query}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
