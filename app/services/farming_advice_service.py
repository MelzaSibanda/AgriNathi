class FarmingAdviceService:
    """Service for generating farming advice based on queries"""

    def __init__(self):
        self.knowledge_base = {
            # Planting and timing
            'plant': 'Planting advice: Choose the right season for each crop. Most vegetables grow best in spring and summer.',
            'when to plant': 'Planting timing: Check local climate and soil temperature. Spring is generally best for most crops.',
            'tomato': 'Tomatoes: Plant between May and June when soil is warm (above 15°C). Space plants 45-60cm apart.',
            'maize': 'Maize: Plant in November-December after last frost. Needs well-drained soil and regular watering.',
            'potato': 'Potatoes: Plant in winter (June-August) in cooler areas. Use certified seed potatoes.',
            'beans': 'Beans: Plant in spring after frost danger has passed. They fix nitrogen in the soil.',
            'cabbage': 'Cabbage: Plant in autumn or early winter. Needs rich soil and consistent moisture.',
            'spinach': 'Spinach: Plant in autumn and winter. Prefers cool weather and partial shade.',
            'carrot': 'Carrots: Plant in autumn or early winter. Needs loose, sandy soil.',
            'onion': 'Onions: Plant in autumn for summer harvest. Needs full sun and well-drained soil.',

            # Soil and fertilization
            'soil': 'Soil management: Test your soil pH (ideal 6.0-7.0). Add organic matter like compost regularly.',
            'fertilizer': 'Fertilization: Use balanced NPK fertilizer. Apply during growing season, not too close to harvest.',
            'compost': 'Composting: Mix green and brown materials. Turn pile regularly. Use after 2-3 months.',
            'ph': 'Soil pH: Most vegetables prefer slightly acidic to neutral soil (pH 6.0-7.0).',
            'organic': 'Organic farming: Use natural methods like compost, neem oil, and beneficial insects.',

            # Watering
            'water': 'Watering: Water deeply but infrequently. Early morning is best to reduce evaporation.',
            'drought': 'Drought management: Mulch to retain moisture. Water deeply at roots. Choose drought-tolerant varieties.',
            'irrigation': 'Irrigation: Drip irrigation is most efficient. Avoid wetting leaves to prevent diseases.',

            # Pest and disease control
            'pest': 'Pest control: Use integrated pest management. Introduce beneficial insects. Use organic sprays.',
            'disease': 'Disease prevention: Plant disease-resistant varieties. Ensure good air circulation. Remove affected plants.',
            'fungus': 'Fungal diseases: Improve air circulation. Avoid overhead watering. Use copper-based fungicides.',
            'insect': 'Insect pests: Use neem oil spray. Encourage ladybugs and other beneficial insects.',
            'weed': 'Weed control: Mulch to suppress weeds. Hand weed regularly. Use organic herbicides.',

            # Weather and climate
            'frost': 'Frost protection: Cover plants with frost cloth. Use row covers. Plant frost-tolerant varieties.',
            'rain': 'Heavy rain: Ensure good drainage to prevent root rot. Raised beds help in wet areas.',
            'wind': 'Wind protection: Plant windbreaks. Stake tall plants. Use mulch to protect soil.',

            # Harvesting and storage
            'harvest': 'Harvesting: Harvest at peak ripeness. Use clean tools. Store in cool, dry place.',
            'storage': 'Storage: Keep vegetables in cool, humid conditions. Use proper containers to prevent spoilage.',
            'seed': 'Seed saving: Save seeds from healthy plants. Dry thoroughly before storing in cool place.',

            # General farming
            'sustainable': 'Sustainable farming: Rotate crops, use organic methods, conserve water, protect soil.',
            'organic': 'Organic certification: Follow organic standards, keep records, avoid synthetic chemicals.',
            'small scale': 'Small-scale farming: Start small, learn as you grow, focus on high-value crops.',
        }

    def get_advice(self, query):
        """Get farming advice based on user query"""
        query_lower = query.lower()

        # Direct keyword matching
        for keyword, advice in self.knowledge_base.items():
            if keyword in query_lower:
                return advice

        # Crop-specific advice
        crops = ['tomato', 'maize', 'potato', 'beans', 'cabbage', 'spinach', 'carrot', 'onion']
        for crop in crops:
            if crop in query_lower:
                return f"For {crop}es: {self.knowledge_base.get(crop, 'Consult local agricultural extension services for specific advice.')}"

        # Seasonal advice
        if any(word in query_lower for word in ['when', 'season', 'time', 'planting']):
            return "Planting seasons vary by crop and location. Check local climate and soil conditions."

        # Default advice
        return "General farming advice: Practice sustainable agriculture, monitor your crops regularly, maintain soil health, and consult local extension services for specific guidance."

    def get_comprehensive_advice(self, query):
        """Get more detailed advice with multiple points"""
        base_advice = self.get_advice(query)

        # Add additional tips based on context
        additional_tips = []

        query_lower = query.lower()

        if 'plant' in query_lower or 'seed' in query_lower:
            additional_tips.extend([
                "Ensure proper seed spacing for good air circulation.",
                "Water gently after planting to settle soil around roots.",
                "Label your plantings with dates and varieties."
            ])

        if 'water' in query_lower or 'irrigation' in query_lower:
            additional_tips.extend([
                "Check soil moisture by inserting finger 5cm deep.",
                "Water at soil level, not on leaves, to prevent diseases.",
                "Mulch helps retain soil moisture and suppress weeds."
            ])

        if 'pest' in query_lower or 'disease' in query_lower:
            additional_tips.extend([
                "Regular monitoring is key to early detection.",
                "Remove and destroy affected plant parts immediately.",
                "Practice crop rotation to break pest and disease cycles."
            ])

        if additional_tips:
            return base_advice + " Additional tips: " + " ".join(additional_tips)
        else:
            return base_advice