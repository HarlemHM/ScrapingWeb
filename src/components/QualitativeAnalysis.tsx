import { MessageSquare, ThumbsUp, ThumbsDown, Clock, Star, Calendar, Quote, ChevronDown } from "lucide-react";
import { useState } from "react";

interface Review {
  hotel: string;
  text: string;
  rating: number;
  date?: string;
  platform: "google" | "booking" | "airbnb";
}

interface QualitativeAnalysisProps {
  positiveReviews: Review[];
  negativeReviews: Review[];
  recentReviews: Review[];
}

const INITIAL_DISPLAY = 20;
const LOAD_MORE_INCREMENT = 20;

export function QualitativeAnalysis({ positiveReviews, negativeReviews, recentReviews }: QualitativeAnalysisProps) {
  const [positiveShown, setPositiveShown] = useState(INITIAL_DISPLAY);
  const [negativeShown, setNegativeShown] = useState(INITIAL_DISPLAY);
  const [recentShown, setRecentShown] = useState(INITIAL_DISPLAY);

  const renderStars = (rating: number) => {
    return '★'.repeat(Math.round(rating));
  };

  const ReviewCard = ({ review, borderColor, bgColor }: { review: Review; borderColor: string; bgColor: string }) => (
    <div className={`${bgColor} p-5 rounded-xl border-l-4 ${borderColor} hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1`}>
      <div className="flex items-center gap-2 mb-3">
        <Quote className="h-4 w-4 text-gray-400" />
        <div className="font-semibold text-sm text-gray-700">{review.hotel}</div>
        <span className="text-xs px-2 py-1 bg-white rounded-full text-gray-600">{review.platform}</span>
      </div>
      <p className="text-sm text-gray-800 mb-4 leading-relaxed italic">"{review.text}"</p>
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Star className="h-4 w-4 text-yellow-500" />
          <span className="text-yellow-500 font-medium">{renderStars(review.rating)}</span>
          <span className="text-xs text-gray-500">({review.rating.toFixed(1)}/5)</span>
        </div>
        {review.date && (
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Calendar className="h-3 w-3" />
            <span>{review.date}</span>
          </div>
        )}
      </div>
    </div>
  );

  const LoadMoreButton = ({ 
    onClick, 
    shown, 
    total, 
    color 
  }: { 
    onClick: () => void; 
    shown: number; 
    total: number; 
    color: string;
  }) => {
    if (shown >= total) return null;
    
    return (
      <button
        onClick={onClick}
        className={`w-full mt-4 py-3 px-4 bg-gradient-to-r ${color} text-white rounded-lg hover:shadow-lg transition-all duration-300 flex items-center justify-center gap-2 font-medium`}
      >
        <ChevronDown className="h-5 w-5" />
        Ver más ({total - shown} restantes)
      </button>
    );
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-xl card-shadow p-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg">
            <MessageSquare className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-gray-800">
              Análisis Cualitativo
            </h2>
            <p className="text-gray-600">
              Análisis detallado de reseñas categorizadas por sentimiento
            </p>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Reseñas Más Positivas */}
        <div className="bg-white rounded-xl card-shadow hover:card-shadow-hover transition-all duration-300 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-green-100 rounded-lg">
              <ThumbsUp className="h-5 w-5 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-green-600">Reseñas Positivas</h3>
            <span className="ml-auto text-sm text-gray-500">({positiveReviews.length} total)</span>
          </div>
          <div className="space-y-4">
            {positiveReviews.length > 0 ? (
              <>
                {positiveReviews.slice(0, positiveShown).map((review, index) => (
                  <ReviewCard 
                    key={`positive-${index}`}
                    review={review} 
                    borderColor="border-green-500" 
                    bgColor="bg-gradient-to-r from-green-50 to-green-100"
                  />
                ))}
                <LoadMoreButton
                  onClick={() => setPositiveShown(prev => prev + LOAD_MORE_INCREMENT)}
                  shown={positiveShown}
                  total={positiveReviews.length}
                  color="from-green-500 to-green-600"
                />
              </>
            ) : (
              <div className="text-center py-12">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                  <ThumbsUp className="h-8 w-8 text-gray-400" />
                </div>
                <p className="text-gray-500">No hay reseñas positivas disponibles</p>
              </div>
            )}
          </div>
        </div>

        {/* Reseñas Más Negativas */}
        <div className="bg-white rounded-xl card-shadow hover:card-shadow-hover transition-all duration-300 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-red-100 rounded-lg">
              <ThumbsDown className="h-5 w-5 text-red-600" />
            </div>
            <h3 className="text-lg font-semibold text-red-600">Reseñas Negativas</h3>
            <span className="ml-auto text-sm text-gray-500">({negativeReviews.length} total)</span>
          </div>
          <div className="space-y-4">
            {negativeReviews.length > 0 ? (
              <>
                {negativeReviews.slice(0, negativeShown).map((review, index) => (
                  <ReviewCard 
                    key={`negative-${index}`}
                    review={review} 
                    borderColor="border-red-500" 
                    bgColor="bg-gradient-to-r from-red-50 to-red-100"
                  />
                ))}
                <LoadMoreButton
                  onClick={() => setNegativeShown(prev => prev + LOAD_MORE_INCREMENT)}
                  shown={negativeShown}
                  total={negativeReviews.length}
                  color="from-red-500 to-red-600"
                />
              </>
            ) : (
              <div className="text-center py-12">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                  <ThumbsDown className="h-8 w-8 text-gray-400" />
                </div>
                <p className="text-gray-500">No hay reseñas negativas</p>
              </div>
            )}
          </div>
        </div>

        {/* Reseñas Recientes */}
        <div className="bg-white rounded-xl card-shadow hover:card-shadow-hover transition-all duration-300 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Clock className="h-5 w-5 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-blue-600">Reseñas Recientes</h3>
            <span className="ml-auto text-sm text-gray-500">({recentReviews.length} total)</span>
          </div>
          <div className="space-y-4">
            {recentReviews.length > 0 ? (
              <>
                {recentReviews.slice(0, recentShown).map((review, index) => (
                  <ReviewCard 
                    key={`recent-${index}`}
                    review={review} 
                    borderColor="border-blue-500" 
                    bgColor="bg-gradient-to-r from-blue-50 to-blue-100"
                  />
                ))}
                <LoadMoreButton
                  onClick={() => setRecentShown(prev => prev + LOAD_MORE_INCREMENT)}
                  shown={recentShown}
                  total={recentReviews.length}
                  color="from-blue-500 to-blue-600"
                />
              </>
            ) : (
              <div className="text-center py-12">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                  <Clock className="h-8 w-8 text-gray-400" />
                </div>
                <p className="text-gray-500">No hay reseñas recientes disponibles</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Summary Analytics */}
      <div className="bg-white rounded-xl card-shadow p-6">
        <div className="flex items-center gap-2 mb-6">
          <MessageSquare className="h-5 w-5 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-800">
            Resumen de Análisis
          </h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-3xl font-bold text-green-600">{positiveReviews.length}</div>
                <div className="text-sm text-green-700 font-medium">Reseñas Positivas</div>
              </div>
              <div className="p-3 bg-green-200 rounded-lg">
                <ThumbsUp className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-xl border border-red-200 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-3xl font-bold text-red-600">{negativeReviews.length}</div>
                <div className="text-sm text-red-700 font-medium">Reseñas Negativas</div>
              </div>
              <div className="p-3 bg-red-200 rounded-lg">
                <ThumbsDown className="h-6 w-6 text-red-600" />
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-3xl font-bold text-blue-600">{recentReviews.length}</div>
                <div className="text-sm text-blue-700 font-medium">Reseñas Recientes</div>
              </div>
              <div className="p-3 bg-blue-200 rounded-lg">
                <Clock className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}