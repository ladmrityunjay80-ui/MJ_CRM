import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { MoreHorizontal, DollarSign, Calendar } from 'lucide-react';
import { format } from 'date-fns';
import { dealsService } from '../services';

interface Deal {
  id: string;
  name: string;
  value: number;
  currency: string;
  stage: string;
  probability: number;
  expected_close_date: string | null;
  company_name?: string;
  contact_name?: string;
}

const STAGES = ['prospecting', 'qualification', 'proposal', 'negotiation', 'won', 'lost'];
const STAGE_COLORS = {
  prospecting: 'bg-blue-100 border-blue-300',
  qualification: 'bg-purple-100 border-purple-300',
  proposal: 'bg-yellow-100 border-yellow-300',
  negotiation: 'bg-orange-100 border-orange-300',
  won: 'bg-green-100 border-green-300',
  lost: 'bg-red-100 border-red-300',
};

export default function DealsKanban() {
  const queryClient = useQueryClient();
  const [draggedDeal, setDraggedDeal] = useState<Deal | null>(null);

  const { data: deals, isLoading } = useQuery({
    queryKey: ['deals'],
    queryFn: () => dealsService.getAll(),
  });

  const updateDealMutation = useMutation({
    mutationFn: ({ id, stage }: { id: string; stage: string }) =>
      dealsService.update(id, { stage }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] });
    },
  });

  const handleDragStart = (deal: Deal) => {
    setDraggedDeal(deal);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (stage: string) => {
    if (draggedDeal && draggedDeal.stage !== stage) {
      updateDealMutation.mutate({ id: draggedDeal.id, stage });
    }
    setDraggedDeal(null);
  };

  const getDealsByStage = (stage: string) => {
    return deals?.filter((deal: Deal) => deal.stage === stage) || [];
  };

  const getStageTotal = (stage: string) => {
    return getDealsByStage(stage).reduce((sum: number, deal: Deal) => sum + deal.value, 0);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Deals Pipeline</h1>
        <p className="text-gray-600 mt-1">Drag and drop deals to update their stage</p>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4">
        {STAGES.map((stage) => {
          const stageDeals = getDealsByStage(stage);
          const stageTotal = getStageTotal(stage);

          return (
            <div
              key={stage}
              className={`flex-shrink-0 w-80 rounded-lg border-2 p-4 ${STAGE_COLORS[stage as keyof typeof STAGE_COLORS]}`}
              onDragOver={handleDragOver}
              onDrop={() => handleDrop(stage)}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-gray-800 capitalize">{stage}</h2>
                <span className="text-sm text-gray-600">{stageDeals.length}</span>
              </div>

              <div className="text-sm text-gray-600 mb-4">
                Total: ${stageTotal.toLocaleString()}
              </div>

              <div className="space-y-3">
                {stageDeals.map((deal: Deal) => (
                  <div
                    key={deal.id}
                    draggable
                    onDragStart={() => handleDragStart(deal)}
                    className="bg-white rounded-lg p-4 shadow-sm cursor-move hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-medium text-gray-900 flex-1">{deal.name}</h3>
                      <button className="text-gray-400 hover:text-gray-600">
                        <MoreHorizontal className="w-4 h-4" />
                      </button>
                    </div>

                    <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
                      <DollarSign className="w-4 h-4" />
                      <span>{deal.currency} {deal.value.toLocaleString()}</span>
                    </div>

                    {deal.company_name && (
                      <div className="text-sm text-gray-600 mb-2">
                        {deal.company_name}
                      </div>
                    )}

                    {deal.expected_close_date && (
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Calendar className="w-4 h-4" />
                        <span>{format(new Date(deal.expected_close_date), 'MMM d, yyyy')}</span>
                      </div>
                    )}

                    <div className="mt-3">
                      <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                        <span>Probability</span>
                        <span>{deal.probability}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all"
                          style={{ width: `${deal.probability}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}

                {stageDeals.length === 0 && (
                  <div className="text-center py-8 text-gray-500 text-sm">
                    No deals in this stage
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
